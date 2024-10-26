from rest_framework import serializers
from subsplease.models import *
from anilist.models import *
from django.utils import timezone

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
    pub_date = serializers.SerializerMethodField()
    episode_num = serializers.SerializerMethodField()
    simple_title = serializers.CharField(source="guid.simple_title", read_only=True)
    icon_url = serializers.CharField(source='anime.icon_url')

    def get_episode_num(self, obj):
        # prevent cyclic import
        from transmission.views import get_episode_num_from_torrent
        return get_episode_num_from_torrent(obj.guid.full_title)

    def get_pub_date(self, obj):
        pub_date = obj.guid.pub_date
        django_timezone = timezone.get_current_timezone()
        pub_date_tz = pub_date.replace(tzinfo=django_timezone)
        
        pub_date_fmt = pub_date_tz.strftime("%B %d %Y - %I:%M %p %Z")

        return pub_date_fmt

    class Meta:
        model = Download
        fields = ['guid', 'anime', 'tid', 'release_title', 'pub_date', 'episode_num', "simple_title", "icon_url"]