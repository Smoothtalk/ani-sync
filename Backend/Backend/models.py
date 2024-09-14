from django.db import models

# Create your models here.

class Backend(models.Model):
    url = models.CharField(max_length=200)