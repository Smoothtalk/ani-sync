from django.db import models

FINISHED = "FIN"
RELEASING = "REL"
NOT_YET_RELEASED = "NYR"
CANCELLED = "CAN"
HIATUS = "HIA"

STATUS = [
("FIN", "FINISHED"),
("REL", "RELEASED"),
("NYR", "NOT_YET_RELEASED"),
("CAN", "CANCELLED"),
("HIA", "HIATUS"),
]

# Create your models here.
class AniList_User(models.Model):
    anilist_user_name = models.CharField(max_length=200)

class Anime(models.Model):
    show_id = models.IntegerField()
    title = models.CharField(max_length=300)
    alt_title = models.JSONField(blank=True)
    status = models.CharField(max_length=3, choices=STATUS, default=NOT_YET_RELEASED)

    def convert_status(long_value):
        print(dict(STATUS)[long_value])

class User_Anime(models.Model):
    watcher = models.ForeignKey("AniList_User", on_delete=models.CASCADE)
    show_id = models.ForeignKey("Anime", on_delete=models.CASCADE)
    custom_titles = models.JSONField()
    last_watched_episode = models.SmallIntegerField()