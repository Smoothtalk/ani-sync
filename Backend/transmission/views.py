import transmission_rpc
import paramiko
import os
import environ
import threading
import re
import requests
import time
import sys

from cryptography.fernet import Fernet

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q

from collections import OrderedDict

from transmission.models import *
from transmission.serializers import download_serializaer, recent_download_serializer
from subsplease.models import Url
from anilist.models import User_Anime, AniList_User
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event


def index(request):
    return HttpResponse("Hello, world. You're at the transmission index.")

class Transmission(APIView):

    def get(self, request):
        transmission_obj = Setting.objects.get()
    
        transmission_client = connect_to_transmission(transmission_obj.address, transmission_obj.port)
        
        host_download_dir = transmission_client.get_session().download_dir
        
        retroactive_days = Url.objects.get().retroactive_days

        if(transmission_obj.ssh_key_passphrase == None or transmission_obj.ssh_key_passphrase == ''):
            encrypt_ssh_passphrase(transmission_obj)
        
        if(transmission_obj.host_download_dir != host_download_dir):
            transmission_obj.host_download_dir = host_download_dir
            transmission_obj.save()

        # Get the current time
        now = timezone.now()

        # Calculate the time three days ago
        now = timezone.localtime(timezone.now())
        days_ago = now - timedelta(days=retroactive_days)
        last_variable_days_downloads = Download.objects.filter(guid__pub_date__gte=days_ago)

        downloads = create_download_db_objects(retroactive_days)

        latest_downloads_first = last_variable_days_downloads.order_by('-guid__pub_date')

        serializer = download_serializaer(latest_downloads_first, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class Recent_Download_Torrents(APIView):
    def get(self, request):
        req_username = request.GET.get('username')

        if not AniList_User.objects.filter(user_name=req_username).exists():
            return Response("Error no username provided", status=status.HTTP_400_BAD_REQUEST)
        else:
            current_or_pln_user_anime = User_Anime.objects.filter(watcher__user_name=req_username, watching_status__in=["CUR", "PLN"]).values_list('show_id', flat=True)
            recently_downloaded_cur_pln_anime = Download.objects.filter(anime__in=current_or_pln_user_anime).order_by('-guid__pub_date')
            serialized_downloads = recent_download_serializer(recently_downloaded_cur_pln_anime, many=True)

            return Response(serialized_downloads.data, status=status.HTTP_200_OK)

class Current_Torrents_Downloads(APIView):
    def get(self, request):
        req_username = request.GET.get('username')

        if not AniList_User.objects.filter(user_name=req_username).exists():
            return Response("Error no username provided", status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict = {}

            transmission_obj = Setting.objects.get()
            transmission_client = connect_to_transmission(transmission_obj.address, transmission_obj.port)

            # change to this after done building, will get recent ones while building
            # downloads = Download.objects.filter(Q(tid__isnull=True) | Q(tid=""))downloads = Download.objects.filter(Q(tid__isnull=True) | Q(tid=""))
            last_3_releases = Release.objects.order_by('-pub_date')[:3]

            # check the current torrents downloading
            # if any of the full titles/links match our last 3 releases, further process
            # in the further processing, get the current % and return that in a dict of simple title

            for torrent in transmission_client.get_torrents():
                for release in last_3_releases:
                    if(release.full_title == torrent.name):
                        episode = release.simple_title + " - " + get_episode_num_from_torrent(torrent.name)
                        resp_dict.update({episode: torrent.percent_complete * 100})

            return Response(resp_dict, status=status.HTTP_200_OK)

class Current_File_Transfers(APIView):

    transfers = {}

    def get(self, request):
        req_username = request.GET.get('username')

        if not AniList_User.objects.filter(user_name=req_username).exists():
            return Response("Error no username provided", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(self.transfers, status=status.HTTP_200_OK)

class Download_Torrents(APIView):
    lock = threading.Lock()

    def get(self, request):
        transmission_obj = Setting.objects.get()
        transmission_client = connect_to_transmission(transmission_obj.address, transmission_obj.port)

        downloads = Download.objects.filter(Q(tid__isnull=True) | Q(tid=""))
        serializer = download_serializaer(downloads, many=True)

        torrents = []
        threads = []
        for download in downloads:
            torrent_download_dict = add_new_download_to_transmission(transmission_client, download)
            torrents.append(torrent_download_dict)

        # from main thread spawn a new monitor thread
        # once all threads are done
        # print("torrents: ")
        # print(torrents)0
        
        # Use ThreadPoolExecutor for managing threads
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit process_torrent tasks to the executor
            futures = [
                executor.submit(process_torrent, transmission_client, torrent_download_dict)
                for torrent_download_dict in torrents
            ]

            # Wait for all threads to complete
            for future in as_completed(futures):
                try:
                    result = future.result()  # Retrieves the result or raises an exception if one occurred
                    print(f"Thread result: {result}")
                except Exception as e:
                    print(f"Error occurred in thread: {str(e)}")

        return Response(serializer.data, status=status.HTTP_200_OK) 

class Current_File_Transfers(APIView):
    transfers = {}
    lock = threading.Lock()
    line_order = []  # Order of titles added

def process_torrent(transmission_client, torrent_download_dict):
    torrent = torrent_download_dict['torrent']
    download = torrent_download_dict['download']
    transmission_host_settings = Setting.objects.get()

    client_torrent = transmission_client.get_torrent(torrent.hash_string)

    # wait till torrent is populated with stats and files
    while(len(client_torrent.file_stats) < 1):
        client_torrent = update_torrent(transmission_client, torrent.hash_string)
        time.sleep(0.1)

    # get the total size of torrent
    torrent_size = get_torrent_size(client_torrent)

    # wait till torrent is done
    while(client_torrent.progress < 100.00 and (not client_torrent.seeding or client_torrent.stopped)):
        print_progress_bar_new(client_torrent.file_stats[0].bytesCompleted, torrent_size, torrent.name)
        client_torrent = update_torrent(transmission_client, torrent.hash_string)
        time.sleep(1)

    transmission_host_connection = connect_to_transmission_host(transmission_host_settings.address, transmission_host_settings.host_download_username, transmission_host_settings.ssh_key_path, transmission_host_settings.ssh_key_passphrase)

    try:
        # add to current transfers dict
        release_obj = Release.objects.get(guid=download.guid.guid)
        episode_number = get_episode_num_from_torrent(torrent.name)

        # Current_File_Transfers.transfers[release_obj.simple_title + ' - ' + episode_number] = 0

        move_to_remote_file_server(torrent, download, transmission_host_settings, transmission_host_connection, client_torrent.total_size)
        delete_new_download_from_transmission(transmission_client, torrent)
        add_tid_to_download(torrent, download)
        print("Done syncing: " + torrent.name)

        # remove from current transfers dict
        # Current_File_Transfers.transfers.pop(download.anime.title + ' - ' + episode_number)

        # send async post api discord here later3
        post_data = {
        'torrent': {
            'hash_string': torrent.hash_string,
            'name': torrent.name
            }
        }

        # Call Discord post method via internal POST request
        try:
            response = requests.post('http://localhost:8000/discord_api/announce_to_discord/', json=post_data)  # Assuming you're running locally
            if response.status_code == 200:
                print(response.text)
            else:
                print(response.text)
        except Exception as e:
           print(f"Error occurred while calling Discord API: {str(e)}")
    finally: 
        disconnect_from_transmission_host(transmission_host_connection)

def move_to_remote_file_server(torrent, download, transmission_obj, transmission_host_connection, torrent_size):
    remote_download_dir = transmission_obj.remote_download_dir
    host_download_dir = transmission_obj.host_download_dir

    release_obj = Release.objects.get(guid=download.guid.guid)
    episode_number = get_episode_num_from_torrent(torrent.name)

    if episode_number is None:
        episode_number = ""

    command = ("mkdir -p " +'\'' + remote_download_dir + release_obj.simple_title + '\'')
    stdout = execute_ssh_command(transmission_host_connection, command)

    command = ("chown 1002:1003 "+ '\'' + remote_download_dir + release_obj.simple_title + '\'')
    stdout = execute_ssh_command(transmission_host_connection, command)

    # command = "cp \'" + host_download_dir + '/' + torrent.name + "\' \'" + remote_download_dir + release_obj.simple_title + '\''
    # TODO write documentation about gcp
    copy_command = ("cp " 
               '\'' + host_download_dir + '/' + torrent.name + '\'' 
               + ' '
               +'\'' + remote_download_dir + release_obj.simple_title + '\''
               )

    #TODO move copy command into copy thread, the join will deal with not mv till done. TEST THIS SHIT
    copy_progress_thread = threading.Thread(
       target=monitor_copy, 
       args=(transmission_host_connection, (remote_download_dir + release_obj.simple_title + '/' + torrent.name), torrent_size, release_obj.simple_title + ' - ' + episode_number)
    )
    copy_progress_thread.start()

    stdout = execute_ssh_command(transmission_host_connection, copy_command)
    
    copy_progress_thread.join()

    command = ("mv " 
    + '\'' + remote_download_dir + release_obj.simple_title + '/' + torrent.name + '\'' 
    + ' '
    + '\'' + remote_download_dir + release_obj.simple_title + '/' + release_obj.simple_title + ' - ' + episode_number + '.mkv' + '\''
    )
    stdout = execute_ssh_command(transmission_host_connection, command)

    command = ("chown 1002:1003 " 
    +'\'' + remote_download_dir + release_obj.simple_title + '/' + release_obj.simple_title + ' - ' + episode_number + '.mkv' + '\''
    )
    stdout = execute_ssh_command(transmission_host_connection, command)

    command = ("chmod 0770 " 
    + '\'' + remote_download_dir + release_obj.simple_title + '/' + release_obj.simple_title + ' - ' + episode_number + '.mkv' + '\''
    )
    stdout = execute_ssh_command(transmission_host_connection, command)

def execute_ssh_command(transmission_host_connection, command):
    stdin, stdout, stderr = transmission_host_connection.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    
    if exit_status != 0:
        print(f"Command failed: {command}\nSTDERR: {stderr.read().decode()}")
        # logging.error(f"Command failed: {command}\nSTDERR: {stderr.read().decode()}")
    
    print("Command: " + command)
    print("STDOUT: " + stdout.read().decode())
    print("STDERR: " + stderr.read().decode())
    return stdout

def monitor_copy(transmission_host_connection, remote_file_path, total_size, title):
    current_size = 0
    last_size = 0
    unchanged_duration = 0 
    timeout = 60
 
    while current_size < total_size:
        try:
            # Current_File_Transfers.transfers.update({title : (current_size / total_size) * 100})
            current_size = get_remote_file_size(transmission_host_connection, remote_file_path)
            print_progress_bar_new(current_size, total_size, title)
        except:
            print("\rWaiting for file to appear...", end="")

        # Check if the size has changed
        if current_size > last_size:
            last_size = current_size  # Update the last known size
            unchanged_duration = 0  # Reset the unchanged duration counter
        else:
            unchanged_duration += 1
        
        # Check if the unchanged duration exceeds the timeout
        if unchanged_duration >= timeout:
            print("\nTransfer failed: File size did not increase within timeout!")
            return
        
        time.sleep(1)  # Poll every second

def get_remote_file_size(transmission_host_connection, remote_file_path):
    """
    Get the size of a file on the remote server.

    Args:
        transmission_host_connection: The SSH connection.
        remote_file_path: Path to the file on the remote server.

    Returns:
        The size of the file in bytes.
    """
    command = f"stat -c%s '{remote_file_path}'"
    stdin, stdout, stderr = transmission_host_connection.exec_command(command)
    size_output = stdout.read().decode().strip()
    return int(size_output) if size_output.isdigit() else 0

def print_progress_bar_new(current_bytes, total_bytes, title):
    current_mb = current_bytes / (1024 * 1024)
    total_mb = total_bytes / (1024 * 1024) if total_bytes else 1  # Avoid division by zero
    percent = (current_mb / total_mb) * 100

    bar = f"{title[:60]:<60} [{int(percent):3}%] {current_mb:.1f}/{total_mb:.1f} MB"

    with Current_File_Transfers.lock:
        if title not in Current_File_Transfers.transfers:
            Current_File_Transfers.transfers[title] = percent
            Current_File_Transfers.line_order.append(title)
        else:
            Current_File_Transfers.transfers[title] = percent

        line_index = Current_File_Transfers.line_order.index(title)
        total_lines = len(Current_File_Transfers.line_order)
        lines_up = total_lines - line_index

        # Move up to the correct line
        sys.stdout.write(f"\033[{lines_up}F")  # Cursor up
        sys.stdout.write("\033[K")             # Clear line
        sys.stdout.write(f"{bar}\n")           # Print progress bar

        # Move back down to the bottom
        if lines_up > 1:
            sys.stdout.write(f"\033[{lines_up - 1}E")
        sys.stdout.flush()

def print_progress_bar(current, total, title, bar_length=40):
    """
    Print a progress bar to the console.

    Args:
        current: Current progress (in bytes).
        total: Total size (in bytes).
        bar_length: Length of the progress bar in characters.
    """
    progress = current / total
    block = int(bar_length * progress)
    bar = f"[{'#' * block}{'-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(f"\r{title} - {bar}")
    sys.stdout.flush()

def create_download_db_objects(retroactive_days):
    # get releases
    # check which releases are not in downloads, by comparing guid
    # for every gui not in releases make a list, create download objs and serialize save
    # return download objs

    # Find all releases where the guid is not present in the Download table

    downloads = []

    # Get the current time
    now = timezone.now()

    # Calculate the time three days ago
    now = timezone.localtime(timezone.now())
    three_days_ago = now - timedelta(days=retroactive_days)
    last_three_days_releases = Release.objects.filter(pub_date__gte=three_days_ago)

    for release in last_three_days_releases:
        new_download = OrderedDict([('guid', None), ('anime', None), ('tid', None)])
        
        new_download['guid'] = release.guid
        new_download['anime'] = release.anime.pk

        serializer = download_serializaer(data=new_download)

        existing_download = Download.objects.filter(guid=new_download['guid']).exists()

        if serializer.is_valid():
            if not existing_download:
                serializer.save()
        downloads.append(new_download)

    return downloads

def connect_to_transmission(address, port):
    return transmission_rpc.Client(host=address, port=port)

def update_torrent(transmission_client, torrent_hash_string):
    return transmission_client.get_torrent(torrent_hash_string)

def get_torrent_size(torrent):
    # bytes
    torrent_size = 0

    for file in torrent.get_files():
        torrent_size = file.size
    
    return torrent_size

def add_new_download_to_transmission(client, download):
    # add to transmission
    # send move to remote file server
    # make sure torrent is not already in , won't happen because we exclude releases already saved in downloads

    # print(download['anime'])
    # print(client.get_torrents())
    # added_torrent = 
    # print(download['link'])
    new_torrent = client.add_torrent(download.guid.link)

    return {"torrent" : new_torrent, "download" : download}

def add_tid_to_download(torrent, download):
    download_from_db = Download.objects.get(guid=download.guid)
    
    #save tid to download obj using serializer
    updated_data = {'tid' : torrent.hash_string}

    serializer = download_serializaer(download_from_db, data=updated_data, partial=True)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

def encrypt_ssh_passphrase(settings_obj):
    env = environ.Env()
    environ.Env.read_env()

    ssh_key_passkey= env("ssh_key_passphase_encrpt_key").encode()
    cipher_suite = Fernet(ssh_key_passkey)

    # Encrypt the passphrase

    passphrase = env("ssh_key_passphrase")
    encrypted_passphrase = cipher_suite.encrypt(passphrase.encode())
    encrypted_passphrase = str(encrypted_passphrase)[2:-1]

    # Store the encrypted passphrase in the database
    settings_obj.ssh_key_passphrase = encrypted_passphrase
    settings_obj.save()

def decrypt_ssh_passphrase(encrypted_passphrase):
    env = environ.Env()
    environ.Env.read_env()

    print('\ndecrypting passphrase')
    encryption_key = env("ssh_key_passphase_encrpt_key").encode()
    cipher_suite = Fernet(encryption_key)
    decrypted_passphrase = cipher_suite.decrypt(encrypted_passphrase).decode()

    return decrypted_passphrase

def connect_to_transmission_host(address, username, ssh_key_path, encrypted_passphrase):
    # somehow connect securely to transmission command shell with key file or hashed 
    # check if windows or linux 

    paramiko.util.log_to_file("paramiko.log")
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        private_key = paramiko.RSAKey.from_private_key_file(os.getcwd() + ssh_key_path, password=decrypt_ssh_passphrase(encrypted_passphrase))

        ssh_client.connect(address, username=username, pkey=private_key)

        # stdin, stdout, stderr = ssh_client.exec_command('ls')
        # print(stdout.read().decode())

        # ssh_client.close
        return ssh_client
    except paramiko.AuthenticationException:
        print("SSH Authentication failed")
        # logging.error("SSH Authentication failed")
    except Exception as e:
        print(f"SSH connection error: {str(e)}")
        # logging.error(f"SSH connection error: {str(e)}")

def delete_new_download_from_transmission(client, torrent):
    client.remove_torrent(torrent.hash_string, delete_data=True)

def disconnect_from_transmission_host(transmission_host_connection):
    transmission_host_connection.close()

def get_host_download_dir(client):
    return client.get_session().download_dir

def get_episode_num_from_torrent(torrent_name):
    match = re.search(r'-\s([\d]+(?:\.\d+)?(?:v\d+)?)\s\(', torrent_name)
    if match:
        return match.group(1)
    return None

def get_download_db_objects():
    pass    # ensure /etc/ssh/sshd_config PubkeyAuthentication yes 