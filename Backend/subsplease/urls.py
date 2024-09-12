from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("get_magnet_links/", SubsPlease.as_view(), name="get_magnet_links")
]
