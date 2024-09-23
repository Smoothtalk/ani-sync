from rest_framework import serializers
from anilist.models import AniList_User, Anime, User_Anime, WATCHING_STATUS, AIRING_STATUS

class anilist_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = AniList_User 
        fields = '__all__'

class anime_serializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'

class user_anime_serializer(serializers.ModelSerializer):
    anime_title = serializers.CharField(source='show_id.title', read_only=True)
    watcher_username = serializers.CharField(source='watcher.user_name', read_only=True)
    anime_status = serializers.SerializerMethodField()
    watching_status = serializers.SerializerMethodField()
    
    class Meta:
        model = User_Anime
        fields = ['watcher', 'show_id', 'watching_status', 'custom_titles', 'last_watched_episode', 
                  'anime_title', 'anime_status', 'watcher_username']

    # Custom method to get the expanded airing status (anime_status)
    def get_anime_status(self, obj):
        return obj.show_id.get_status_display() 

    # Custom method to get the expanded watching status
    def get_watching_status(self, obj):
        return obj.get_watching_status_display()
