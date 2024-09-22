from django.db import models
from subsplease.models import Release
from anilist.models import Anime

# Create your models here.

class Discord_API(models.Model):
    discord_bot_token = models.CharField(max_length=64, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Discord Setting'
        verbose_name_plural = 'Discord Settings'
    