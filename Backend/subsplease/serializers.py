from rest_framework import serializers
from subsplease.models import SubsPlease

class SubsPlease_serializer(serializers.ModelSerializer):
    class Meta:
        model = SubsPlease 
        fields = '__all__'

