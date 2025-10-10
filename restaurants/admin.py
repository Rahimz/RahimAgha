from django.contrib import admin

from .models import Place, Category, Review, ReviewItem, Vote , VoteResponse
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'active',]    

@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'item_type', 'is_applicable']    


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'review', 'user',]    
    


@admin.register(VoteResponse)
class VoteResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'vote', 'review_item', 'score',]    
    