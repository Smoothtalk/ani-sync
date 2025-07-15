from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.core.management import call_command

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collections import OrderedDict
from anilist.serializers import *
# Create your views here.


class SyncAnimeView(APIView):
    def post(self, request):

        username = request.data.get("username")
        try:
            call_command("sync_anime", "--user", username)
            return Response({"message": f"sync_anime of {username}"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def index(request):
    return HttpResponse("Hello, world. You're at the Live Backend index.")

@csrf_protect
def login_user(request):
    # print(request.headers)
    print("CSRF Cookie:", request.COOKIES.get("csrftoken"))
    if request.method == "POST": 
        req_username = request.POST.get("username") 
        req_password = request.POST.get('password')

        user_in_db = authenticate(request=request, username=req_username, password=req_password)

        if(user_in_db is not None):
            login(request, user_in_db)
            return JsonResponse(data={}, status=status.HTTP_200_OK)
        
    return HttpResponse(status=status.HTTP_410_GONE)

@csrf_protect  
def new_user(request):
    if request.method == 'POST':

        try:
            data = JSONParser().parse(request)  # Parse JSON data
            username = data.get("username")
            password = data.get("password")
            discord_id = data.get("discord_id")

            # Create a django user 
            django_user = User.objects.create_user(username=username, password=password)
            django_user.save()

            try:
                anilist_user = AniList_User.objects.get(user_name=username)
                print(anilist_user)
                anilist_user.user = django_user
                # add django user to anilist_user
                # continue on
            except AniList_User.DoesNotExist:
                print("User DNE")
                anilist_user = OrderedDict([("user", django_user.pk), ("user_name", username), ("discord_user_id", discord_id)])

            #link to anilist user
            serializer = anilist_user_serializer(data=anilist_user)

            if serializer.is_valid():
                serializer.save() 
            else:
                print(serializer.errors)

            login(request, django_user)
            
            return JsonResponse({"message": "User created successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_protect   
def logout_user(request):
    logout(request)  # Clears the session and removes sessionid
    
    response = JsonResponse({'message': 'Logged out successfully'})
    response.delete_cookie("csrftoken")
    
    return response

@ensure_csrf_cookie  
def serve_csrf_cookie(request):
    token = get_token(request)
    return JsonResponse({"csrfToken": token})
