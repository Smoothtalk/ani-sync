from django.db import models

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
    user_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user_name}"
    
    class Meta:
        verbose_name = 'AniList_User'
        verbose_name_plural = 'AniList_Users'

class Anime(models.Model):
    show_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1000)
    alt_titles = models.JSONField(default=list, blank=True, null=False)
    status = models.CharField(max_length=3, choices=AIRING_STATUS, default=NOT_YET_RELEASED)

    def convert_status_to_db(long_value):
        return [status for status in AIRING_STATUS if status[1] == long_value][0][0]
    
    def __str__(self):
        return f"{self.title}"

class User_Anime(models.Model):
    class Meta:
        models.UniqueConstraint(fields = ['watcher', 'show_id'], name = 'compisite_pk')

    watcher = models.ForeignKey("AniList_User", on_delete=models.CASCADE)
    show_id = models.ForeignKey("Anime", on_delete=models.CASCADE)
    watching_status = models.CharField(max_length=3, choices=WATCHING_STATUS, default=PLANNING)
    custom_titles = models.JSONField() #user added custom titles
    last_watched_episode = models.SmallIntegerField()

    def convert_status_to_db(long_value):
        return [status for status in WATCHING_STATUS if status[1] == long_value][0][0]

    def __str__(self):
        match self.watching_status:
            case "CUR":
                return f"{str(self.watcher) + " is watching " + str(self.show_id)}"
            case "PLN":
                return f"{str(self.watcher) + " is planning to watch " + str(self.show_id)}"
            case "CPL":
                return f"{str(self.watcher) + " has completed watching " + str(self.show_id)}"
            case "DRP":
                return f"{str(self.watcher) + " has dropped watching " + str(self.show_id)}"
            case "PAU":
                return f"{str(self.watcher) + " has paused watching " + str(self.show_id)}"
            case "RPR":
                return f"{str(self.watcher) + " is repeat watching " + str(self.show_id)}"


    class Meta:
        verbose_name = 'User_Anime'
        verbose_name_plural = 'User_Animes'
