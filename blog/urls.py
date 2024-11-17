from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('<str:slug>/', views.BlogPostView, name='blog_post'),
    path('', views.BlogPostListView, name='blog_posts'),
]
