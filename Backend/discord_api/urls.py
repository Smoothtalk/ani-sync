from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("announce_to_discord/", Discord_Class.as_view(), name="announce_discord")
]
