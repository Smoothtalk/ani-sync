from django.contrib import admin
from anilist.models import Anime, AniList_User, User_Anime

# Register your models here.
admin.site.register(Anime)
admin.site.register(AniList_User)
admin.site.register(User_Anime)