from rest_framework import serializers
from subsplease.models import *
from anilist.models import *
from transmission.models import *

class setting_serializaer(serializers.ModelSerializer):
    class Meta:
        models = Setting
        fields = '__all__'

class download_serializaer(serializers.ModelSerializer):
    anime = serializers.CharField(source='anime.title')

    class Meta:
        model = Download
        fields = ['guid', 'anime', 'url']