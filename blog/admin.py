from django.contrib import admin

from .models import Post, PostCategory, Attachment

class AttachmentInline(admin.StackedInline):
    model = Attachment
    raw_id_fields = ('post',)
    extra = 2


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'rank', ]

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    prepopulated_fields = {"slug": ["name"]}
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'rank', 'show_date', 'published']
    list_editable = ['rank', 'show_date']
    prepopulated_fields = {"slug": ["title"]}
    inlines = [AttachmentInline]
    
