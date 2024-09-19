from django.contrib import admin

from .models import GeoRecord


@admin.register(GeoRecord)
class GeoRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'country', 'ip', 'created']