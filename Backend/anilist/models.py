from django.db import models

# Create your models here.
class AniList_User(models.Model):
    anilist_user_name = models.CharField(max_length=200)

class Anime(models.Model):
    FINISHED = "FIN"
    RELEASING = "REL"
    NOT_YET_RELEASED = "NYR"
    CANCELLED = "CAN"
    HIATUS = "HIA"

    STATUS = [
    ("FIN", "Finished"),
    ("REL", "Releasing"),
    ("NYR", "Not yet Released"),
    ("CAN", "Cancelled"),
    ("HIA", "Hiatus"),
    ]

    show_id = models.IntegerField()
    title = models.CharField(max_length=300)
    alt_title = models.JSONField()
    status = models.CharField(max_length=3, choices=STATUS, default=NOT_YET_RELEASED)


class User_Anime(models.Model):
    watcher = models.ForeignKey("AniList_User", on_delete=models.CASCADE)
    show_id = models.ForeignKey("Anime", on_delete=models.CASCADE)
    custom_titles = models.JSONField()
    last_watched_episode = models.SmallIntegerField()