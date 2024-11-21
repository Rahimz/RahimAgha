from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('<str:slug>/', views.BlogPostView, name='blog_post'),
    path('', views.BlogPostListView, name='blog_posts'),
    
    path('<str:slug>/type/<str:attach_type>/', views.BlogPostView, name='blog_post_type'),
    path('change-rank/<int:attach_id>/<str:dir>/', views.ChangeAttachmentRankView, name='blog_attach_rank_change'),
]
