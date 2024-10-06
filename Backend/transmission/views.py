import transmission_rpc
import paramiko
import os
import environ
import threading
import re
import requests

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
from transmission.serializers import download_serializaer
from subsplease.models import Url

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
        
class Download_Torrents(APIView):
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
        for torrent_download_dict in torrents:
            thread = threading.Thread(target=monitor_torrent, args=(transmission_client, torrent_download_dict,))
            thread.start()
            threads.append(thread)

        # block till all syncing is done
        for thread in threads:
            thread.join()

        return Response(serializer.data, status=status.HTTP_200_OK) 

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

def get_host_download_dir(client):
    return client.get_session().download_dir

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

def delete_new_download_from_transmission(client, torrent):
    client.remove_torrent(torrent.hash_string, delete_data=True)

def monitor_torrent(transmission_client, torrent_download_dict):
    torrent = torrent_download_dict['torrent']
    download = torrent_download_dict['download']

    client_torrent = transmission_client.get_torrent(torrent.hash_string)

    # might need to adjust this
    while(not client_torrent.seeding and client_torrent.progress < 100.00):
        client_torrent = transmission_client.get_torrent(torrent.hash_string)

    transmission_obj = Setting.objects.get()
    transmission_host_connection = connect_to_transmission_host(transmission_obj.address, transmission_obj.host_download_username, transmission_obj.ssh_key_path, transmission_obj.ssh_key_passphrase)
    
    move_to_remote_file_server(torrent, download, transmission_obj.remote_download_dir, transmission_obj.host_download_dir, transmission_host_connection)
    delete_new_download_from_transmission(transmission_client, torrent)
   
    print("Done syncing: " + torrent.name)

    add_tid_to_download(torrent, download)

    # send async post api discord here later
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

def move_to_remote_file_server(torrent, download, remote_download_dir, host_download_dir, transmission_host_connection):
    release_obj = Release.objects.get(guid=download.guid.guid)
    episode_number = get_episode_num_from_torrent(torrent.name)

    command = ("mkdir -p " 
               +'\'' + remote_download_dir + release_obj.simple_title + '\'')
    stdin, stdout, stderr = transmission_host_connection.exec_command(command)
    print("Command: " + command)
    print("STDOUT: " + stdout.read().decode())
    print("STDERR: " + stderr.read().decode())

    command = ("chown 1000:1000 "
               + '\'' + remote_download_dir + release_obj.simple_title + '\''
                )
    stdin, stdout, stderr = transmission_host_connection.exec_command(command)

    # command = "cp \'" + host_download_dir + '/' + torrent.name + "\' \'" + remote_download_dir + release_obj.simple_title + '\''
    # TODO write documentation about gcp
    command = ("cp " 
               '\'' + host_download_dir + '/' + torrent.name + '\'' 
               + ' '
               +'\'' + remote_download_dir + release_obj.simple_title + '\''
               )
    print("Command: " + command)
    print("STDOUT: " + stdout.read().decode())
    print("STDERR: " + stderr.read().decode())
    
    stdin, stdout, stderr = transmission_host_connection.exec_command(command)

    # need to confirm that the cp is done
    exit_status = stdout.channel.recv_exit_status()  

    if exit_status == 0:
        command = ("mv " 
        + '\'' + remote_download_dir + release_obj.simple_title + '/' + torrent.name + '\'' 
        + ' '
        + '\'' + remote_download_dir + release_obj.simple_title + '/' + release_obj.simple_title + ' - ' + episode_number + '.mkv' + '\''
        )

        stdin, stdout, stderr = transmission_host_connection.exec_command(command)  
        # print("Command: " + command)
        # print("STDOUT: " + stdout.read().decode())
        # print("STDERR: " + stderr.read().decode())

        command = ("chown 1000:1000 " 
        +'\'' + remote_download_dir + release_obj.simple_title + '/' + release_obj.simple_title + ' - ' + episode_number + '.mkv' + '\''
        )
        stdin, stdout, stderr = transmission_host_connection.exec_command(command)
        # print("Command: " + command)
        # print("STDOUT: " + stdout.read().decode())
        # print("STDERR: " + stderr.read().decode())

        command = ("chmod 0770 " 
        + '\'' + remote_download_dir + release_obj.simple_title + '/' + release_obj.simple_title + ' - ' + episode_number + '.mkv' + '\''
        )
        stdin, stdout, stderr = transmission_host_connection.exec_command(command)
        # print("Command: " + command)
        # print("STDOUT: " + stdout.read().decode())
        # print("STDERR: " + stderr.read().decode())

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

    print('decrypting passphrase')
    encryption_key = env("ssh_key_passphase_encrpt_key").encode()
    cipher_suite = Fernet(encryption_key)
    decrypted_passphrase = cipher_suite.decrypt(encrypted_passphrase).decode()

    return decrypted_passphrase

def connect_to_transmission_host(address, username, ssh_key_path, encrypted_passphrase):
    # somehow connect securely to transmission command shell with key file or hashed 
    # check if windows or linux 

    paramiko.util.log_to_file("paramiko.log")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    private_key = paramiko.RSAKey.from_private_key_file(os.getcwd() + ssh_key_path, password=decrypt_ssh_passphrase(encrypted_passphrase))

    ssh_client.connect(address, username=username, pkey=private_key)

    return ssh_client
    # stdin, stdout, stderr = ssh_client.exec_command('ls')
    # print(stdout.read().decode())
    # ssh_client.close

def get_episode_num_from_torrent(torrent_name):
    match = re.search(r'-\s([\d]+(?:\.\d+)?(?:v\d+)?)\s\(', torrent_name)
    if match:
        return match.group(1)
    return None

def get_download_db_objects():
    pass    # ensure /etc/ssh/sshd_config PubkeyAuthentication yes 
