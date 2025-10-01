from django.contrib import admin

from .models import Place
from .forms import PlaceAdminForm

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ['uuid', 'name', 'active', 'city']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name', 'description', 'city']