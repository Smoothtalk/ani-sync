from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("get_downloads/", Transmission.as_view(), name="get_downloads"),
    path("get_recent_downloads/", Recent_Download_Torrents.as_view(), name="recent_download_releases"),
    path("download_releases/", Download_Torrents.as_view(), name="download_releases")
]
