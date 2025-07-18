"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("csrf/", views.serve_csrf_cookie, name="serve_csrf_cookie"),
    path("user/new_user/", views.new_user, name="new_user"),
    path("user/login/", views.login_user, name="login_user"),
    path("user/logout/", views.logout_user, name="logout_user"),
    path("sync/", SyncAnimeView.as_view(), name="sync_anime"),
    path('admin/', admin.site.urls),
    path("transmission/", include("transmission.urls")),    
    path("anilist/", include("anilist.urls")),
    path("subsplease/", include("subsplease.urls")),
    path("discord_api/", include("discord_api.urls")),
]
