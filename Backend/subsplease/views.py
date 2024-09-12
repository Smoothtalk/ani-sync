import feedparser
import json
import itertools
from fuzzywuzzy import fuzz
from subsplease.models import *
from subsplease.serializers import release_serializer
from anilist.models import User_Anime, Anime

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from collections import OrderedDict

from datetime import datetime

# Create your views here.

# TODO CHANGE FUZZ RATIO INTO DATABASE FIELD
FUZZ_RATIO = 75

def index(request):
    return HttpResponse("Hello, world. You're at the SubsPlease index.")

class SubsPlease(APIView):

    # feedparser.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    feedparser.USER_AGENT = user_agent

    def get(self, request):
        # get the releases from urls
        # TODO handle multiple URLS, only support for 1 now

        # TODO try catch here for failure, table empty & DNE
        urls = Url.objects.all()

        for url in urls:
            feed = feedparser.parse(url.feed_url)
            print("Status of RSS Feed: " + str(feed.status))
            releases = feed.get('entries')
            create_releases_db_objects(releases)

        return Response("Test", status=status.HTTP_200_OK)
    
def create_releases_db_objects(releases_str):
    # Add new releases to db
    # make sure to add it to the anime too
    # might need fuzzy matching
    # print(json.dumps(releases_str, indent=2))

    serialized_releases = []
    anime_titles = get_all_cur_pln_titles()

    for release in releases_str:
        simple_title = trim_simple_title(release['tags'][0]['term'])
        django_datetime = convert_datetime(release['published'])

        new_release = OrderedDict([('full_title', release['title']), ('link', release['link']), ('guid', release['id']), ('pub_date', django_datetime), ('simple_title', simple_title)])
        serializer = release_serializer(data=new_release)

        existing_entry = Release.objects.filter(guid=new_release['guid']).exists()

        if serializer.is_valid() and not existing_entry:
            serialized_releases.append(new_release)

            # add to Anilist_anime here
            find_anilist_showid_from_title(simple_title, anime_titles)

            # serializer.save()
        elif len(serializer.errors) > 0:
            print(serializer.errors)

def convert_datetime(date_time_str):
    date_format = "%a, %d %b %Y %H:%M:%S %z"

    date_obj = datetime.strptime(date_time_str, date_format)

    return date_obj

def trim_simple_title(simple_title):
    if('Atri' in simple_title):
        print('x')

    trimmed_string, _, _ = simple_title.rpartition(' - ')
    return trimmed_string

# TODO extensive testing needed
# need to add custom titles and alt title support
# return anilist.anime obj, empty or one instance
def find_anilist_showid_from_title(release_title, anime_titles):
    # need to somehow get title, alt_titles, and custom_titles
    # then use fuzzywuzzy to determine if there's a match
    # if not return empty obj
    release_title = release_title.lower()
        
    for title in anime_titles:
        if(fuzz.ratio(title, release_title) > FUZZ_RATIO):
            print("Match with - Title: " + title + " and release title: " + release_title)

    # user_anime_obj = User_Anime.objects.filter(Q(show_id__title__iexact=anime_title) & (Q(watching_status='CUR') | Q(watching_status='PLN')))
    
    # # title didn't find it, check alt titles
    # # TODO fix this
    # if not user_anime_obj.exists():
    #     user_anime_obj = User_Anime.objects.filter(Q(show_id__alt_titles__in=anime_title) & (Q(watching_status='CUR') | Q(watching_status='PLN')))

    # # title didn't find it, check custom titles
    # if not user_anime_obj.exists():
    #     user_anime_obj = User_Anime.objects.filter(custom_titles__in=anime_title)

    # print("release title:", anime_title)

    # if user_anime_obj.exists():
    #     print(user_anime_obj.get().show_id)
        # print(user_anime_obj)
        # print(user_anime_obj.get().show_id_id)
        # anime_obj = Anime.objects.filter(show_id=user_anime_obj.show_id)
        # print(anime_obj)

    return -1

def get_all_cur_pln_titles():
    anime_titles = []

    # get titles
    user_anime_cur_pln_titles = User_Anime.objects.filter((Q(watching_status='CUR') | Q(watching_status='PLN')))
    
    # since title is always one, simple make a list from that
    anime_titles = [user_anime.show_id.title for user_anime in user_anime_cur_pln_titles]

    #get alt_titles
    user_anime_cur_pln_alt_titles = User_Anime.objects.filter((Q(watching_status='CUR') | Q(watching_status='PLN')))
    
    # add alt titles, if there are more than one, flatten them
    anime_alt_titles = list(itertools.chain.from_iterable(
        [user_anime.show_id.alt_titles if isinstance(user_anime.show_id.alt_titles, list) else [user_anime.show_id.alt_titles] 
        for user_anime in user_anime_cur_pln_alt_titles]
    ))

    #remove empty values
    anime_alt_titles = [title for title in anime_alt_titles if title]
    
    #TODO test when custom title is included
    user_anime_cur_pln_custom_titles = User_Anime.objects.filter((Q(watching_status='CUR') | Q(watching_status='PLN')))
    anime_custom_titles = list(itertools.chain.from_iterable(
        [user_anime.custom_titles for user_anime in user_anime_cur_pln_custom_titles if user_anime.custom_titles]
    ))

    combined_list = [item for sublist in [anime_titles, anime_alt_titles, anime_custom_titles] if sublist for item in sublist if item]

    return combined_list