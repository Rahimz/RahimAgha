from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.VideoListView, name='video_list')
]
