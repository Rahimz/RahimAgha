from django.contrib import admin

from .models import Place, Category
from .forms import PlaceAdminForm

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ['uuid', 'name', 'active', 'city']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name', 'description', 'city']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order',]
    list_editable = ['order']
    prepopulated_fields = {'slug': ['name']}