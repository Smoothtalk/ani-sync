from django.db import models
from subsplease.models import Release
from anilist.models import Anime

# Create your models here.

class Setting(models.Model):
    port = models.PositiveIntegerField(default=51413)
    address = models.CharField(max_length=200)

    def __str__(self):
       return f"{self.address + ':' + str(self.port)}"
    
    class Meta:
        verbose_name = 'Transmission Setting'
        verbose_name_plural = 'Transmission Settings'
    
class Download(models.Model):
    guid = models.ForeignKey(Release, related_name="download_id", on_delete=models.CASCADE, default='')
    anime = models.ForeignKey(Anime, related_name="download_anime_title", on_delete=models.CASCADE, default='')
    url = models.ForeignKey(Release, related_name="download_link", on_delete=models.CASCADE, default='')

    def __str__(self):
       return f"{'Downloaded: ' + self.anime + ' (' + str(self.guid) + ')'}"
    
    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
    