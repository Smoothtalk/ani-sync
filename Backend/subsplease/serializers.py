from rest_framework import serializers
from subsplease.models import *


class url_serializer(serializers.ModelSerializer):
    class Meta:
        model = Url 
        fields = '__all__'

class release_serializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = '__all__'

