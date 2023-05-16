from django.db import models

# Create your models here.
class User(models.Model):
    anilist_user_name = models.CharField(max_length=200)
    custom_titles = models.JSONField()

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

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    show_id = models.IntegerField()
    title = models.CharField(max_length=300)
    alt_title = models.JSONField()
    status = models.CharField(max_length=3, choice=STATUS, default=NOT_YET_RELEASED)
    last_watched_episode = models.SmallIntegerField()