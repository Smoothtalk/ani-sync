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

class recent_download_serializer(serializers.ModelSerializer):
    anime = serializers.PrimaryKeyRelatedField(queryset=Anime.objects.all())
    release_title = serializers.CharField(source='guid.full_title', read_only=True)
    pub_date = serializers.DateTimeField(source='guid.pub_date', read_only=True)
    episode_num = serializers.SerializerMethodField()
    simple_title = serializers.CharField(source="guid.simple_title", read_only=True)

    def get_episode_num(self, obj):
        # prevent cyclic import
        from transmission.views import get_episode_num_from_torrent
        return get_episode_num_from_torrent(obj.guid.full_title)

    class Meta:
        model = Download
        fields = ['guid', 'anime', 'tid', 'release_title', 'pub_date', 'episode_num', "simple_title"]