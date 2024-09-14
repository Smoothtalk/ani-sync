import transmission_rpc

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from collections import OrderedDict

from transmission.models import *
from transmission.serializers import download_serializaer
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the transmission index.")

class Transmission(APIView):

    def get(self, request):

        transmission_obj = Setting.objects.get()
    
        transmission_client = connect_to_transmission(transmission_obj.address, transmission_obj.port)
        downloads = create_download_db_objects()
        return Response(downloads, status=status.HTTP_200_OK)
    
def connect_to_transmission(address, port):
    return transmission_rpc.Client(host=address, port=port)

def create_download_db_objects():
    # get releases
    # check which releases are not in downloads, by comparing guid
    # for every gui not in releases make a list, create download objs and serialize save
    # return download objs

    # Find all releases where the guid is not present in the Download table

    downloads = []

    releases_not_in_downloads = Release.objects.exclude(guid__in=Download.objects.values('guid'))

    for release in releases_not_in_downloads:
        new_download = OrderedDict([('guid', None), ('anime', None), ('link', None)])
        
        new_download['guid'] = release.guid
        new_download['anime'] = release.anime.title
        new_download['link'] = release.link

        serializer = download_serializaer(data=new_download)

        existing_download = Download.objects.filter(guid=new_download['guid']).exists()

        if serializer.is_valid() and not existing_download:
            downloads.append(new_download)
            # serializer.save()
        else:
            print(serializer.errors)
        
    return downloads

def get_download_db_objects():
    pass