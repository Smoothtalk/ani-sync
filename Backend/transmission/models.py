from django.db import models
from subsplease.models import Release
from anilist.models import Anime

# Create your models here.

class Setting(models.Model):
    port = models.PositiveIntegerField(default=51413)
    address = models.CharField(max_length=200)
    remote_download_dir = models.CharField(max_length=1000, null=True) # if you need anything big, you got bigger problems
    host_download_dir = models.CharField(max_length=1000, null=True)
    ssh_key_path = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=100, default='')
    ssh_key_passphrase = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
       return f"{self.address + ':' + str(self.port)}"
    
    class Meta:
        verbose_name = 'Transmission Setting'
        verbose_name_plural = 'Transmission Settings'
    
class Download(models.Model):
    guid = models.ForeignKey(Release, related_name="download_id", on_delete=models.CASCADE, default='')
    anime = models.ForeignKey(Anime, related_name="download_anime_title", on_delete=models.CASCADE, default='')
    tid = models.CharField(max_length=40, default='', null=True, blank=True)

    def __str__(self):
       return f"{'Downloaded: ' + str(self.guid)}"
    
    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
    