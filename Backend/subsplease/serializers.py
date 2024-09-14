from rest_framework import serializers
from subsplease.models import *
from anilist.models import *
from anilist.serializers import anime_serializer

class url_serializer(serializers.ModelSerializer):
    class Meta:
        model = Url 
        fields = '__all__'

class release_serializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(queryset=Anime.objects.all())
    
    class Meta:
        model = Release
        fields = ['full_title', 'link', 'guid', 'pub_date', 'simple_title', 'anime']
