from django.db import models
from django.contrib.auth.models import User

FINISHED = "FIN"
RELEASING = "REL"
NOT_YET_RELEASED = "NYR"
CANCELLED = "CAN"
HIATUS = "HIA"

CURRENT = "CUR"
PLANNING = "PLN"
COMPLETED = "CPL"
DROPPED = "DRP"
PAUSED = "PAU"
REPEATING = "RPR"

WINTER = "Winter"
SPRING = "Spring"
SUMMER = "Summer"
FALL = "Fall"

SEASONS = [
    ("WINTER", "Winter"),
    ("SPRING", "Spring"),
    ("SUMMER", "Summer"),
    ("FALL", "Fall"),
]

AIRING_STATUS = [
    ("FIN", "FINISHED"),
    ("REL", "RELEASING"),
    ("NYR", "NOT_YET_RELEASED"),
    ("CAN", "CANCELLED"),
    ("HIA", "HIATUS"),
]

WATCHING_STATUS = [
    ("CUR", "CURRENT"),
    ("PLN", "PLANNING"),
    ("CPL", "COMPLETED"),
    ("DRP", "DROPPED"),
    ("PAU", "PAUSED"),
    ("RPR", "REPEATING"),
]


# Create your models here.
class AniList_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=200, unique=True)
    discord_user_id = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f"{self.user_name}"
    
    class Meta:
        verbose_name = 'AniList_User'
        verbose_name_plural = 'AniList_Users'

class Anime(models.Model):
    show_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1000)
    alt_titles = models.JSONField(default=list, blank=True, null=True)
    status = models.CharField(max_length=3, choices=AIRING_STATUS, default=NOT_YET_RELEASED)
    season = models.CharField(max_length=6, choices=SEASONS, null=True)
    season_year = models.SmallIntegerField(null=True)
    icon_url = models.CharField(max_length=2000, null=True)
    
    def convert_status_to_db(long_value):
        for status in AIRING_STATUS:
            if status[1] == long_value:
                return status[0]
        raise ValueError(f"Invalid status: {long_value}")
    
    def convert_status_from_db(short_value):
        for status in AIRING_STATUS:
            if status[0] == short_value:
                return status[1]
        raise ValueError(f"Invalid status: {short_value}")
    
    def __str__(self):
        return f"{self.title}"

class User_Anime(models.Model):
    class Meta:
        models.UniqueConstraint(fields = ['watcher', 'show_id'], name = 'compisite_pk')

    watcher = models.ForeignKey("AniList_User", on_delete=models.CASCADE)
    show_id = models.ForeignKey("Anime", on_delete=models.CASCADE)
    watching_status = models.CharField(max_length=3, choices=WATCHING_STATUS)
    custom_titles = models.JSONField(default=list, blank=True, null=True) #user added custom titles
    last_watched_episode = models.SmallIntegerField()

    def convert_status_to_db(long_value):
        for status in WATCHING_STATUS:
            if status[1] == long_value:
                return status[0]
        raise ValueError(f"Invalid status: {long_value}")
    
    def convert_status_from_db(short_value):
        for status in WATCHING_STATUS:
            if status[0] == short_value:
                return status[1]
        raise ValueError(f"Invalid status: {short_value}")
            
    def __str__(self):
        match self.watching_status:
            case "CUR":
                return f"{str(self.watcher)} is watching {str(self.show_id)}"
            case "PLN":
                return f"{str(self.watcher)} is planning to watch {str(self.show_id)}"
            case "CPL":
                return f"{str(self.watcher)} has completed watching {str(self.show_id)}"
            case "DRP":
                return f"{str(self.watcher)} has dropped watching {(self.show_id)}"
            case "PAU":
                return f"{str(self.watcher)} has paused watching {(self.show_id)}"
            case "RPR":
                return f"{str(self.watcher)} is repeat watching {(self.show_id)}"


    class Meta:
        verbose_name = 'User_Anime'
        verbose_name_plural = 'User_Animes'
