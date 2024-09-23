import re
import subprocess
import asyncio
import os
import platform

from adrf.views import APIView
from asgiref.sync import sync_to_async

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response

from anilist.models import AniList_User
from transmission.models import *
from discord_api.models import Discord_API

def index(request):
    return HttpResponse("Hello, world. You're at the discord index.")

class Discord_Class(APIView):
    async def post(self, request):
        torrent_data = request.data.get('torrent')  # Expecting the torrent data in POST body
        torrent_hash_string = await self.retrieve(torrent_data['hash_string'])

        download_obj = await sync_to_async(lambda: Download.objects.select_related('guid').get(tid=torrent_hash_string.tid))()
        discord_obj = await sync_to_async(lambda: Discord_API.objects.get())()

        #fix this
        release_obj = await sync_to_async(lambda: Release.objects.get(guid=download_obj.guid.guid))()

        anilist_obj = await sync_to_async(lambda: AniList_User.objects.first())()

        torrent_name = await sync_to_async(lambda: torrent_data['name'])()
        episode_num = await async_get_episode_num_from_torrent(torrent_name)

        # anime_title = await sync_to_async(lambda: download_obj.anime.title)()
        anime_title_with_episode_num = release_obj.simple_title + " - " + episode_num + ".mkv"
        anime_title_with_quotes = f'"{anime_title_with_episode_num}"'
        
        try:
            print("Current Working Dir: " + os.getcwd())
            windows = platform.system() == 'Windows'

            # TODO retest on windows
            if windows:
                activate_script = os.path.join(r'..\anisync-venv' , 'Scripts', 'activate.bat')
                command = ['cmd.exe', '/c', activate_script, '&&', 'python', 'discord_api/scripts/announce.py', discord_obj.discord_bot_token, anime_title_with_quotes, anilist_obj.discord_user_id]
            else:
                # Run the Python interpreter directly from the virtual environment
                venv_python = os.path.join("anisync-venv", 'bin', 'python3')
                command = [venv_python, 'Backend/discord_api/scripts/announce.py', discord_obj.discord_bot_token, anime_title_with_quotes, anilist_obj.discord_user_id]


            # Create a subprocess to execute the command in a shell
            process = subprocess.run(' '.join(command) if platform.system() == 'Windows' else command, 
                                    check=True,
                                    shell=windows,
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    )

            # Capture and print the output
            # stdout, stderr = process.communicate()
            print(process.stdout.decode())
            if process.stderr:
                print("Error:", process.stderr.decode())

            # backup way
            # command = venv_path
            # process = subprocess.call(command, shell=True)

            # command = "python3 Backend/discord_api/scripts/announce.py \"" + discord_obj.discord_bot_token + "\"" + " \"" + anime_title_with_episode_num + "\" \"" + anilist_obj.discord_user_id + "\"" 
            # process = subprocess.call(command, shell=True)

            return Response({"message": "Discord user notified successfully!"}, status=status.HTTP_200_OK)
        except Download.DoesNotExist:
            return Response({"error": "Torrent not found!"}, status=status.HTTP_404_NOT_FOUND)
        except subprocess.TimeoutExpired:
            return Response({"error": "The script timed out."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    async def retrieve(self, hash_string):
        torrent = await Download.objects.filter(tid=hash_string).afirst()
        return torrent

async def async_get_episode_num_from_torrent(torrent_name):
    search_result = await sync_to_async(lambda: re.search(r'-\s(\d+)\s\(', torrent_name))()
    
    if search_result:
        return search_result.group(1)
    else:
        return None  # Handle cases where no match is found
    
async def run_discord_script(token, anime_title, user_id):
    # Call the script using subprocess in a non-blocking way
    process = await asyncio.create_subprocess_exec(
        'python', 'scripts/announce.py', token, anime_title, str(user_id),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        print(f"Error running script: {stderr.decode()}")
    else:
        print(f"Script output: {stdout.decode()}")