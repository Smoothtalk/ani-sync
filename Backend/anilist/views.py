from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, When, Value, IntegerField, Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from anilist.models import *
from anilist.serializers import anime_serializer, user_anime_serializer

from bs4 import BeautifulSoup

from graphql import parse, execute
from graphql.language.printer import print_ast

from collections import OrderedDict

import requests
import json
import xml.etree.ElementTree as ET

def index(request):
    return HttpResponse("Hello, world. You're at the anilist index.")

def anime_icon(request):
  url = "https://graphql.anilist.co"
  query = '''
    query getAnimeIcons($animeid: Int) {
        Media (id: $animeid) {
        coverImage {
            extraLarge
            }
        }
    }
    '''
  
  anime_id = request.GET.get('anime_id')

  # check if anime in db has icon url
  # if so return url
  # if not get url, wait 2 seconds before returning
  # TODO when adding new anime add the icon url

  anime_in_db = Anime.objects.get(show_id=anime_id)

  if(anime_in_db.icon_url != None):
      # return the url
      return HttpResponse(anime_in_db.icon_url , status=status.HTTP_200_OK)
  else:
    #add the url in 
      response = requests.post(url, json={'query': query, 'variables': {"animeid" : anime_id}})
      
      icon_url = response.data['media']['coverImage']['extraLarge']

      anime_in_db.icon_url = icon_url
      anime_in_db.save()

      return HttpResponse(icon_url, status=status.HTTP_200_OK)

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
            anime_status = request.query_params.get('status').upper()

        #TODO change request to anilist_user.username
        anime_list = retrieve_anilist(request.query_params.get('username'), anime_status)
        if(anime_list != ''):
            anime_list = json.loads(anime_list)
            no_errors = False

        # print(json.dumps(anime_list, indent=4))
        
        (no_errors, serialized_ani_list) = create_anime_list_db_objects(anime_list)

        create_user_anime_db_objects(anime_list, anilist_user)

        user_anime_list = user_anime_serializer(get_anime_list_from_db(anilist_user, anime_status), many=True)

        return Response(user_anime_list.data, status=status.HTTP_200_OK)

        # if no_errors == True:
        #     return Response(user_anime_list, status=status.HTTP_200_OK)
        # else: 
        #     return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

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
                    season
                    seasonYear
                    coverImage {extraLarge}
                    }
                }
            }
        }
    }
    '''

    response = requests.post(url, json={'query': animeListQuery, 'variables': listVariables})
    # prettySoup = json.dumps(response.json()['data']['MediaListCollection']['lists'], indent=4)
    # TODO change this to the success code
    if(response.status_code != 403):
        return json.dumps(response.json()['data']['MediaListCollection']['lists'])
    else:
        return ''    

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

            new_anime = OrderedDict([('show_id', -1), ('title', "TEMP"), ('alt_titles', []), ('status', 'NYR'), ('season', None), ('season_year', None), ('icon_url', None)])
            
            new_anime['show_id'] = entry['mediaId']
            new_anime['title'] = entry['media']['title']['romaji']
            new_anime['status'] = Anime.convert_status_to_db(entry['media']['status'])
            new_anime['season'] = entry['media']['season']
            new_anime['season_year'] = entry['media']['seasonYear']
            new_anime['icon_url'] = entry['media']['coverImage']['extraLarge']

            # TODO debugging clutter, remove later
            # if(new_anime['show_id'] == 169441):
            #     print('x')
            # if(type(entry['media']['title']['english']) is None):
            #     print('x')

            #check of synonyms exist for anime (which is a list) 
            if(len(entry['media']['synonyms']) > 0):
                new_anime['alt_titles'].extend(entry['media']['synonyms'])

            # append singular anime english tititle
            if(entry['media']['title']['english'] is not None and len(entry['media']['title']['english']) > 0):
                new_anime['alt_titles'].append(entry['media']['title']['english'])

            # TODO get romaji title from query and also add it here

            try:
                anime_db_entry = Anime.objects.get(show_id=new_anime['show_id'])
            except Anime.DoesNotExist:
                anime_db_entry = None

            if anime_db_entry: #check if fields changed, update if needed
                if has_new_anime_fields_changed(new_anime, anime_db_entry):
                    anime_db_entry.save()
                    serialized_ani_list.append(anime_db_entry)
            else:
                serializer = anime_serializer(data=new_anime)
                if serializer.is_valid():
                    serializer.save() 
                serialized_ani_list.append(new_anime)

                if len(serializer.errors.keys()) > 0:
                    no_errors = False

    return (no_errors, serialized_ani_list)

def create_user_anime_db_objects(anime_list, anilist_user_str):
    # from an anlist user id
    # create an user anime with watcher (anlist user id TODO future make it a list somehow), a show id (user_anime_list's anime id)
    # append any custom ids 
    # TODO POST the data here later
    # add from user_anime_list current episode if it exists 

    serialized_user_anime = []
    anilist_user = AniList_User.objects.get(user_name=anilist_user_str).pk

    for type_dict in anime_list:
        entries = type_dict['entries']
        for entry in entries:
            show_id = Anime.objects.get(show_id=entry['mediaId']).show_id
            status = User_Anime.convert_status_to_db(entry['status'])
            new_user_anime = OrderedDict([('watcher', anilist_user), ('show_id', show_id), ('watching_status', status), ('custom_titles', []), ('last_watched_episode', entry['progress'])])

            try:
                user_anime_db_entry = User_Anime.objects.get(watcher=anilist_user, show_id=show_id)
            except User_Anime.DoesNotExist:
                user_anime_db_entry = None
            
            if user_anime_db_entry:
                if has_new_user_anime_fields_changed(new_user_anime, user_anime_db_entry):
                    user_anime_db_entry.save()
                    serialized_user_anime.append(user_anime_db_entry)

            else:
                serializer = user_anime_serializer(data=new_user_anime) 

                if serializer.is_valid():
                    serializer.save()

                serialized_user_anime.append(new_user_anime)
                
# assuming that we can find the anime_obj in the 
# this might be for optimization, since if nothing has changed we'd be saving every old entry again
def has_new_anime_fields_changed(new_anime, anime_db_obj):
    # Keep track of whether any fields have changed
    has_changed = False

    # Compare each field and update if necessary
    if anime_db_obj.title != new_anime['title']:
        anime_db_obj.title = new_anime['title']
        has_changed = True
    if anime_db_obj.status != new_anime['status']:
        anime_db_obj.status = new_anime['status']
        has_changed = True
    if anime_db_obj.alt_titles != new_anime['alt_titles']:
        anime_db_obj.alt_titles = new_anime['alt_titles']
        has_changed = True
    if anime_db_obj.season != new_anime['season']:
        anime_db_obj.season = new_anime['season']
        has_changed = True
    if anime_db_obj.season_year != new_anime['season_year']:
        anime_db_obj.season_year = new_anime['season_year']
        has_changed = True
    if anime_db_obj.icon_url != new_anime['icon_url']:
        anime_db_obj.icon_url = new_anime['icon_url']
        has_changed = True
    
    return has_changed

def has_new_user_anime_fields_changed(new_user_anime, user_anime_db_obj):
    # Keep track of whether any fields have changed
    has_changed = False

    # Compare each field and update if necessary
    if user_anime_db_obj.last_watched_episode != new_user_anime['last_watched_episode']:
        user_anime_db_obj.last_watched_episode = new_user_anime['last_watched_episode']
        has_changed = True
    if user_anime_db_obj.watching_status != new_user_anime['watching_status']:
        user_anime_db_obj.watching_status = new_user_anime['watching_status']
        has_changed = True
    # if user_anime_db_obj.custom_titles != new_user_anime['custom_titles'] :
    #     user_anime_db_obj.custom_titles.extend(new_user_anime['custom_titles'])
    #     has_changed = True
    
    return has_changed

def get_first_element_graphql_string(graphql_list):
    return graphql_list[1:-1]

def get_anime_list_from_db(anilist_user_str, anime_status):
    custom_order = Case(
        When(watching_status='CUR', then=Value(1)),
        When(watching_status='PLN', then=Value(2)),
        When(watching_status='CPL', then=Value(3)),
        When(watching_status='DRP', then=Value(4)),
        When(watching_status='PAU', then=Value(5)),
        When(watching_status='RPR', then=Value(6)),
        output_field=IntegerField()
    )

    # Prepare the base query
    query = User_Anime.objects.filter(watcher=anilist_user_str)

    # If anime_status is provided, filter by it, otherwise ignore this filter
    if anime_status:
        db_anime_status = User_Anime.convert_status_to_db(anime_status)
        query = query.filter(Q(watching_status=db_anime_status))

    # Apply the custom ordering and return the result
    return query.annotate(custom_order=custom_order).order_by('custom_order')