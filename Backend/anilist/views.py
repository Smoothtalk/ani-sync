from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from anilist.models import AniList_User, Anime, User_Anime
from anilist.serializers import anilist_user_serializer, anime_serializer, user_anime_serializer

from bs4 import BeautifulSoup

from graphql import parse, execute
from graphql.language.printer import print_ast

from collections import OrderedDict

import requests
import json
import xml.etree.ElementTree as ET


def index(request):
    return HttpResponse("Hello, world. You're at the anilist index.")

class AnimeList(APIView):
    
    def get(self, request):
        anime_status = ''

        try:
            anilist_user = AniList_User.objects.get(user_name=request.query_params.get('username'))
            # continue on
        except AniList_User.DoesNotExist:
            print("User DNE")
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        

        if request.query_params.get('status') != None:
            anime_status = request.query_params.get('status')

        #TODO change request to anilist_user.username
        anime_list = json.loads(retrieve_anilist(request.query_params.get('username'), anime_status))
        
        # print(json.dumps(anime_list, indent=4))
        
        (no_errors, serialized_ani_list) = create_anime_list_db_objects(anime_list)
        create_user_anime_db_objects(anime_list, anilist_user)

        if no_errors == True:
            return Response(serialized_ani_list, status=status.HTTP_200_OK)
        else: 
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

def retrieve_anilist(user_name, status=''):
    url = 'https://graphql.anilist.co'

    if status == '':
        listVariables = {
        'userName'          : user_name,
        'type'              : "ANIME",
        }
    else:
        listVariables = {
        'userName'          : user_name,
        'type'              : "ANIME",
        'in_status_list'    : status
        }
    
    animeListQuery = '''
    query getAnimeList ($userName : String, $type : MediaType, $in_status_list : [MediaListStatus]) {
    MediaListCollection (userName : $userName, type : $type, status_in : $in_status_list) {
        lists{
            entries {
                status
                progress
                mediaId
                media {
                    status 
                    synonyms
                    title {romaji, english}
                    startDate {year,month,day}
                    endDate {year,month,day}
                    }
                }
            }
        }
    }
    '''

    response = requests.post(url, json={'query': animeListQuery, 'variables': listVariables})
    # prettySoup = json.dumps(response.json()['data']['MediaListCollection']['lists'], indent=4)

    return json.dumps(response.json()['data']['MediaListCollection']['lists'])

def create_anime_list_db_objects(anime_list):

    no_errors = True
    serialized_ani_list = []

    for type_dict in anime_list:
        entries = type_dict['entries']
        for entry in entries:
            #check if anime exists in db, if not create
            #if anime exists, check if fields have changed (status, titles, start date, end date)

            #check if user_anime entry exists for user and this anime, if not create it
            #if user_anime exists, check if fields have changed (progress)

            # print(entry['media']['title']['romaji'])

            # print(json.dumps(entry, indent=4))

            new_anime = OrderedDict([('show_id', -1), ('title', "TEMP"), ('alt_title', ['']), ('status', 'NYR')])
            
            new_anime['show_id'] = entry['mediaId']
            new_anime['title'] = entry['media']['title']['romaji']
            new_anime['status'] = Anime.convert_status_to_db(entry['media']['status'])

            #check of synonyms exist for anime 
            if(len(entry['media']['synonyms']) != 0):
                new_anime['alt_title'] = entry['media']['synonyms']
                new_anime['alt_title'].append(entry['media']['title']['english'])

            serializer = anime_serializer(data=new_anime)
            if serializer.is_valid():
                serialized_ani_list.append(new_anime)
                serializer.save()
            else:
                serialized_ani_list.append(new_anime)
                if 'already exists' not in serializer.errors['show_id'][0]:
                    no_errors = False

    return (no_errors, serialized_ani_list)

def create_user_anime_db_objects(anime_list, anilist_user_str):
    # from an anlist user id
    # create an user anime with watcher (anlist user id TODO future make it a list somehow), a show id (user_anime_list's anime id)
    # append any custom ids 
    # TODO POST the data here later
    # add from user_anime_list current episode if it exists 

    serialized_user_anime = []
    anilist_user = AniList_User.objects.get(user_name=anilist_user_str).id

    for type_dict in anime_list:
        entries = type_dict['entries']
        for entry in entries:
            show_id = Anime.objects.get(show_id=entry['mediaId']).show_id
            status = User_Anime.convert_status_to_db(entry['status'])
            new_user_anime = OrderedDict([('watcher', anilist_user), ('show_id', show_id), ('watching_status', status), ('custom_titles', ['']), ('last_watched_episode', entry['progress'])])

            serializer = user_anime_serializer(data=new_user_anime)

            existing_entry = User_Anime.objects.filter(watcher=anilist_user, show_id=show_id).exists()

            if serializer.is_valid() and not existing_entry:
                serialized_user_anime.append(new_user_anime)
                serializer.save()
            elif len(serializer.errors) > 0:
                print(serializer.errors)

def get_first_element_graphql_string(graphql_list):
    return graphql_list[1:-1]

