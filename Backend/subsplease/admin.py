from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from subsplease.models import Url, Release

class Release_Admin(admin.ModelAdmin):
    list_display = ["full_title", "pub_date"]

    search_fields = ["anime__title"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-pub_date')

# Register your models here.
admin.site.register(Url)
admin.site.register(Release, Release_Admin)