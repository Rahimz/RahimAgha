from django.contrib import admin
from parler.admin import TranslatableAdmin


from .models import Project, ProjectCategory, Image


class ImageInline(admin.StackedInline):
    model = Image
    raw_field_id = 'project'
    extra = 1
    
    
@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ['name', 'category',  'uuid', 'active']
    readonly_fields = ['uuid']
    
    inlines = [ImageInline]


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(TranslatableAdmin):
    list_display = ['name']