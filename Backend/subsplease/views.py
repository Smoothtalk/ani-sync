import feedparser
import itertools

from nyaapy import anime_site

from Levenshtein import ratio
from subsplease.models import *
from subsplease.serializers import release_serializer
from anilist.models import User_Anime, Anime, AniList_User

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone

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
        # TODO get the user(username) from the request, pass it on the the respective functions
        req_username = request.GET.get('username')

        # get the releases from urls
        # TODO handle multiple URLS, only support for 1 now

        # TODO try catch here for failure, table empty & DNE
        urls = Url.objects.all()

        # TODO implement some sort of caching
        for url in urls:
            feed = feedparser.parse(url.feed_url)
            print("Status of RSS Feed: " + str(feed.status))
            releases = feed.get('entries')
            serialized_releases = create_releases_db_objects(releases, req_username)

        return Response(serialized_releases, status=status.HTTP_200_OK)
    
class Nyaa(APIView):

    def get(self, request):

        # assume series is added to user name & anime
        # get episode count
        # try multiple groups (subsplease, erai-raws, horriblesubs)
        # process till be either get a batch or episode count
        # need to 
        
        search_results = search_subsplease_on_nyaa_for_all_episodes("Slime", "24", "1080p")

        if (len(search_results) == 0):
            return Response([], status=status.HTTP_200_OK)
            # TODO try another group

        process_nyaa_releases(search_results)

        return Response([], status=status.HTTP_200_OK)

def create_releases_db_objects(releases_str, username):
    # Add new releases to db
    # make sure to add it to the anime too
    # might need fuzzy matching
    # print(json.dumps(releases_str, indent=2))

    serialized_releases = []
    releases_arr = []
    
    #TODO change this to use the currently logged in user or the user specified by the syncing anime (it should be the same)
    anime_titles = get_all_cur_pln_titles(username)

    for release in releases_str:
        simple_title = trim_simple_title(release['tags'][0]['term'])
        django_datetime = convert_datetime(release['published'])

        new_release = OrderedDict([('full_title', release['title']), ('link', release['link']), ('guid', release['id']), ('pub_date', django_datetime), ('simple_title', simple_title)])
        
        # add to Anilist_anime here
        anilist_id = find_anilist_showid_from_title(simple_title, anime_titles)

        if(isinstance(anilist_id, int)):
            anime_obj = get_anime_obj_from_anilist_id(anilist_id)
            new_release['anime'] = anime_obj.pk  # Set to the primary key
    
            serializer = release_serializer(data=new_release)

            existing_entry = Release.objects.filter(guid=new_release['guid']).exists()
            
            if serializer.is_valid():
                # print(new_release['simple_title'])
                if not existing_entry:
                    serialized_releases.append(new_release)
                    serializer.save()
            
            releases_arr.append(new_release)   

    return releases_arr

def convert_datetime(date_time_str):
    date_format = "%a, %d %b %Y %H:%M:%S %z"

    date_obj = datetime.strptime(date_time_str, date_format)
    local_dt = timezone.localtime(date_obj)
    return local_dt

def trim_simple_title(simple_title):
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

    for anime_title in anime_titles:
        if(ratio(anime_title.lower(), release_title, score_cutoff=(FUZZ_RATIO / 100)) != 0.0):
            # print("Match with - Anime Title: " + anime_title + " and release title: " + release_title)

            # Need to use user_anime because there may be a match with a custom title and that may not match with any alt title
            # then once we get the user_anime, we can then get the anime using a join from 
            # need to do this custom matching here TODO
            anime_title_match = User_Anime.objects.filter(Q(show_id__title=anime_title))

            # Fetch possible matches from alt_titles and check in Python for case-insensitive match
            possible_alt_title_matches = User_Anime.objects.filter(Q(show_id__alt_titles__contains=[anime_title]))
            possible_custom_title_matches = User_Anime.objects.filter(Q(custom_titles__contains=[anime_title]))

            matching_anime_alt_titles = []
            for user_anime in possible_alt_title_matches:
                alt_titles = user_anime.show_id.alt_titles
                # Case-insensitive match on alt_titles
                if any(anime_title.lower() in alt_title.lower() for alt_title in alt_titles):
                    matching_anime_alt_titles.append(user_anime)
            alt_title_match = User_Anime.objects.filter(id__in=[anime.id for anime in matching_anime_alt_titles])

            matching_anime_custom_titles = []
            for user_anime in possible_custom_title_matches:
                custom_titles = user_anime.custom_titles
                # Case-insensitive match on alt_titles
                if any(anime_title.lower() in custom_title.lower() for custom_title in custom_titles):
                    matching_anime_custom_titles.append(user_anime)
            custom_title_match = User_Anime.objects.filter(id__in=[anime.id for anime in matching_anime_custom_titles])

            # Combine the query results
            user_anime_obj = anime_title_match | alt_title_match | custom_title_match

            if(user_anime_obj.exists()):
                #if two titles return check
                if len(user_anime_obj) > 1:
                    for user_anime in user_anime_obj:
                        if user_anime.watching_status == "CUR" or user_anime.watching_status == "PLN":
                            return user_anime.show_id_id
                else:
                    return user_anime_obj.get().show_id_id
            else:
                return user_anime_obj

def get_anime_obj_from_anilist_id(anilist_id):
    return Anime.objects.get(show_id=anilist_id)

def get_all_cur_pln_titles(username):
    anime_titles = []

    if not AniList_User.objects.filter(user_name=username).exists():
        return "Username not found"
    else:
        username_id = AniList_User.objects.get(user_name=username).id

    # get titles, include currently watching and planning to watch, exclude already finished anime
    user_anime_cur_pln_titles = User_Anime.objects.filter((Q(watching_status='CUR') | Q(watching_status='PLN')) & Q(watcher=username_id))
    # .exclude(show_id__status='FIN')

    # since title is always one, simple make a list from that
    anime_titles = [user_anime.show_id.title for user_anime in user_anime_cur_pln_titles]

    #get alt_titles
    user_anime_cur_pln_alt_titles = User_Anime.objects.filter((Q(watching_status='CUR') | Q(watching_status='PLN')) & Q(watcher=username_id))
    
    # add alt titles, if there are more than one, flatten them
    anime_alt_titles = list(itertools.chain.from_iterable(
        [user_anime.show_id.alt_titles if isinstance(user_anime.show_id.alt_titles, list) else [user_anime.show_id.alt_titles] 
        for user_anime in user_anime_cur_pln_alt_titles]
    ))

    #remove empty values
    anime_alt_titles = [title for title in anime_alt_titles if title]
    
    #TODO test when custom title is included
    user_anime_cur_pln_custom_titles = User_Anime.objects.filter((Q(watching_status='CUR') | Q(watching_status='PLN')) & Q(watcher=username_id))
    anime_custom_titles = list(itertools.chain.from_iterable(
        [user_anime.custom_titles for user_anime in user_anime_cur_pln_custom_titles if user_anime.custom_titles]
    ))

    combined_list = [item for sublist in [anime_titles, anime_alt_titles, anime_custom_titles] if sublist for item in sublist if item]

    return combined_list

def get_current_season():
    # get any currently airing anime
    # get the season/year of that anime, then return 
    # Won't work because some anime run into next season with 12+ episodes

    # currently_airing_anime = Anime.objects.filter(status="REL").first()
    # print("Current Year:", currently_airing_anime.season_year)
    # print("Current Season:", currently_airing_anime.season)

    current_month = datetime.now().month
    current_year = datetime.now().year
    current_season = ""

    if current_month in (1, 2):
        current_season = "Winter"
    elif current_month in 12:
        current_year += 1
        current_season = "Winter"
    elif current_month in (3, 4, 5):
        current_season = "Spring"
    elif current_month in (6, 7, 8):
        current_season = "Summer"
    elif current_month in (9, 10, 11):
        current_season = "Fall"
    else:
        current_season = None

    return {"current_season": current_season, "current_year": current_year}

def get_anime_obj(anilist_id):
    return Anime.objects.get(show_id=anilist_id)

def search_subsplease_on_nyaa_for_all_episodes(title, release_group, resolution):
    string_tuple = (title, release_group, resolution)
    search_string = " ".join(string_tuple)

    results = anime_site.AnimeTorrentSite.search(search_string, category=1, subcategory=2)
    
    return results    

def process_nyaa_releases(search_results):
    
    if(len(search_results) < 1):
        return
    
    if any("Batch" in search_result.name for search_result in search_results):
        print("Batch in results")
        # add batch to torrent
        # need to be able to move whole folder to remote host
        # shouldn't care about names
    else:
        print("Batch not in results")
        highest_seeders = -1
        best_torrent = None

        for result in search_results:
            print(result.name + result.seeders)

            #find highest seeders if a tie pick the newest released one
            if int(result.seeders) > int(highest_seeders):
                highest_seeders = result.seeders
                best_torrent = result
            elif int(result.seeders) == int(highest_seeders):
                result_datetime_obj = datetime.strptime(result.date, '%Y-%m-%d %H:%M')
                best_torrent_datetime_obj = datetime.strptime(best_torrent.date, '%Y-%m-%d %H:%M')

                if result_datetime_obj > best_torrent_datetime_obj:
                    best_torrent = result

        print(best_torrent.seeders)    
        # add each episode
        # treat like new release