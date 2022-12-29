from django.contrib import admin

from .models import Feature, Point , Image

class ImageInline(admin.TabularInline):
    model = Image
    raw_id_fields = ['feature']


class PointInline(admin.TabularInline):
    model = Point
    raw_id_fields = ['feature']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'show_rank', 'published'
    ]
    list_editable = ['published', ]
    search_fields = ['id', 'title', 'description']
    inlines = [ImageInline, PointInline]
#     list_filter = ['active', 'paid', 'status', 'shipping_status', 'approved_date', 'channel' ]

#     class Meta:
#         ordering = ['created']