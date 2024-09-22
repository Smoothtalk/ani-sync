from rest_framework import serializers
from subsplease.models import *
from anilist.models import *
from transmission.models import *

class setting_serializaer(serializers.ModelSerializer):
    class Meta:
        models = Setting
        fields = '__all__'

class download_serializaer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(queryset=Anime.objects.all())
    release_title = serializers.CharField(source='guid.full_title', read_only=True)

    class Meta:
        model = Download
        fields = ['guid', 'anime', 'tid', 'release_title']