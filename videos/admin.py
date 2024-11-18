from django.contrib import admin

from .models import Video



@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'is_protected', 'category', 'website_header', 'created']
    search_fields = ['name', 'id']
    list_editable = ['is_protected', 'website_header']
    ordering = ('-created',)