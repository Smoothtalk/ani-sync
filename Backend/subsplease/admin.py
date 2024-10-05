from django.contrib import admin
from subsplease.models import Url, Release

class Release_Admin(admin.ModelAdmin):
    list_display = ["full_title", "pub_date"]

    search_fields = ["anime__title"]

# Register your models here.
admin.site.register(Url)
admin.site.register(Release, Release_Admin)