from django.db import models
from anilist.models import Anime

# Create your models here.

class Url(models.Model):
    feed_url = models.CharField(max_length=200)
    retroactive_days = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.feed_url.split('r=', 1)[1]}"

class Release(models.Model):
    full_title = models.CharField(max_length=400)
    link = models.CharField(max_length=2048)
    guid = models.CharField(primary_key=True, max_length=32)
    pub_date = models.DateTimeField()
    simple_title = models.CharField(max_length=200)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='releases')

    def __str__(self):
        return f"{self.full_title}"