from rest_framework import serializers
from anilist.models import AniList_User, Anime, User_Anime

class anilist_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = AniList_User 
        fields = '__all__'

class anime_serializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'

class user_anime_serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Anime
        fields = '__all__'

