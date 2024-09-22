from rest_framework import serializers
from subsplease.models import *
from anilist.models import *
from transmission.models import *
from discord_api.models import *

class discord_serializaer(serializers.ModelSerializer):
    class Meta:
        models = Discord_API
        fields = '__all__'