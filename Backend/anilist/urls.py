from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("get_anime_list/", AnimeList.as_view(), name="get_anime_list"),
    path("get_anime_icon/", views.anime_icon, name="get_anime_icon"),
    path("check_login/", views.check_login, name="check_login"),
    path("create_user/", views.create_user, name="create_user"),
]
