from django.db import models

# Create your models here.
class User(models.Model):
    anilist_user_name = models.CharField(max_length=200)
    custom_titles = models.JSONField()

class Anime(models.Model):
    show_id = 
    title =
    alt_title = models.JSONField()
    status = 
    last_watched_episode =