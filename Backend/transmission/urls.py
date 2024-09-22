from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("get_downloads/", Transmission.as_view(), name="get_downloads"),
    path("download_releases/", Download_Torrents.as_view(), name="download_releases")
]
