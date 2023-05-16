from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=200)
    custom_titles = models.DecimalField()

class Anime(models.Model):
