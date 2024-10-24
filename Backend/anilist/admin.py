from django.contrib import admin
from anilist.models import Anime, AniList_User, User_Anime
import datetime

class Anime_Admin(admin.ModelAdmin):
    @admin.display(description="Airing Status")
    def capitalized_airing_status(obj):
        return Anime.convert_status_from_db(obj.status).capitalize().replace('_', ' ')
    
    list_filter = ("status", "season",)

    list_display = [
        "title",
        capitalized_airing_status,
        "season",
        "season_year",
    ]

    search_fields = ["title", "season_year", "alt_titles"]

class User_Anime_Admin(admin.ModelAdmin):
    @admin.display(description="Watching Status")
    def capitalized_watching_status(obj):
        return User_Anime.convert_status_from_db(obj.watching_status).capitalize()
        
    list_display = [
        "watcher",
        "show_id",
        capitalized_watching_status,
        "last_watched_episode",
    ]
    
    list_filter = ["watching_status",]

    list_display_links = ("show_id",)

    search_fields = ["show_id__title"]

# Register your models here.
admin.site.register(Anime, Anime_Admin)
admin.site.register(AniList_User)
admin.site.register(User_Anime, User_Anime_Admin)