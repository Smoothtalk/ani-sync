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


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the anilist index.")

class AnimeList(APIView):
    
    def get(self, request):
        try:
            anilist_user = AniList_User.objects.get(anilist_user_name=request.query_params.get('username'))
            # continue on
        except AniList_User.DoesNotExist:
            print("User DNE")
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        
        status_list = []
        if request.query_params.get('status_list') != None:
            status_list = json.loads(request.query_params.get('status_list'))['statuses']

        #TODO change request to anilist_user.username
        anime_list = retrieve_anilist(request.query_params.get('username'), status_list)

        (no_errors, serialized_ani_list) = create_anime_list_db_objects(anime_list)

        if no_errors == True:
            return Response(serialized_ani_list, status=status.HTTP_200_OK)
        else: 
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

def retrieve_anilist(user_name, status_list=[]):
    url = 'https://graphql.anilist.co'

    if status_list == []:
        listVariables = {
        'userName'          : user_name,
        'type'              : "ANIME",
        }
    else:
        listVariables = {
        'userName'          : user_name,
        'type'              : "ANIME",
        'in_status_list'    : status_list
        }
    
    animeListQuery = '''
    query getAnimeList ($userName : String, $type : MediaType, $in_status_list : [MediaListStatus]) {
    MediaListCollection (userName : $userName, type : $type, status_in : $in_status_list) {
        lists{
            status
            entries {
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

    return json.dumps(response.json()['data']['MediaListCollection']['lists'][0]['entries'])

def create_anime_list_db_objects(animelist):

    no_errors = True
    serialized_ani_list = []

    result_object_list = json.loads(animelist)

    for entry in result_object_list:
        #check if anime exists in db, if not create
        #if anime exists, check if fields have changed (status, titles, start date, end date)

        #check if user_anime entry exists for user and this anime, if not create it
        #if user_anime exists, check if fields have changed (progress)

        print(entry)
        print('\n')

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

def create_user_anime_db_objects():
    pass

def get_first_element_graphql_string(graphql_list):
    return graphql_list[1:-1]
