from django.contrib import admin
from django.db.models import F
from transmission.models import *
from transmission.views import get_episode_num_from_torrent
# Register your models here.

class Download_Admin(admin.ModelAdmin):
    @admin.display(description="Anime")
    def anime_series(obj):
        return obj.anime.title

    @admin.display(description="Episode Number")
    def episode_num(obj):
        return get_episode_num_from_torrent(obj.guid.full_title)

    @admin.display(description="Pub Date")
    def pub_date(obj):
        return obj.guid.pub_date
    
    pub_date.admin_order_field='guid__pub_date'

    def get_queryset(self, request):
        # Annotate the queryset with the related Release's pub_date field
        qs = super().get_queryset(request)
        return qs.annotate(pub_date=F('guid__pub_date'))  # Use FK to get pub_date from Release

    # anime, episode_num, pub date, tid
    list_display = [anime_series, episode_num, pub_date, "tid"]

    list_display_links = ("tid",)


# Register your models here.
admin.site.register(Setting)
admin.site.register(Download, Download_Admin)