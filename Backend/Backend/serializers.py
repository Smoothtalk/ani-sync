from rest_framework import serializers
from subsplease.models import *
from anilist.models import *

# class Backend(serializers.ModelSerializer):
#     anime_title = serializers.CharField(source='anime.title')

#     class Meta:
#         model = Release
#         fields = ['anime_title', 'full_title', 'link', 'guid', 'pub_date'] 

