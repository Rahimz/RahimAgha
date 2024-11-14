from django.contrib import admin
from django.contrib import messages 

from .models import Contact


def mark_as_spam(modeladmin, request, queryset):
    # Perform your action here
    # For example, let's say you want to mark selected objects as active
    queryset_count = queryset.count()
    queryset.update(is_spam=True)  # Assuming your model has an 'active' field
    messages.success(request, f"{queryset_count} items marked as spam.")

mark_as_spam.short_description = "Mark selected items as spam"  # This will be the name displayed in the admin



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title','is_spam', 'is_checked',  'phone', 'email', 'require', 'description', 
    ]
    list_editable = ['is_spam', 'is_checked', ]
    search_fields = ['title', 'phone', 'email', 'description']
    # inlines = [ImageInline, PointInline]
    list_filter = ['is_checked', 'is_spam']
    actions = [mark_as_spam]

