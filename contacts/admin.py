from django.contrib import admin

from .models import Contact



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'require', 'is_checked', 'phone', 'email'
    ]
    list_editable = ['is_checked', ]
    # search_fields = ['id', 'title', 'description']
    # inlines = [ImageInline, PointInline]
#     list_filter = ['active', 'paid', 'status', 'shipping_status', 'approved_date', 'channel' ]

