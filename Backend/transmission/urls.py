from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("download_releases/", Transmission.as_view(), name="download_releases")
]
