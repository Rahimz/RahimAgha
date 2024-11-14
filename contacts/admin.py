from django.contrib import admin

from .models import Contact



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title','is_spam', 'is_checked',  'phone', 'email', 'require', 'description', 
    ]
    list_editable = ['is_spam', 'is_checked', ]
    search_fields = ['title', 'phone', 'email', 'description']
    # inlines = [ImageInline, PointInline]
    list_filter = ['is_checked', 'is_spam']

