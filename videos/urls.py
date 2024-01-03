from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('details/<uuid:uuid>/', views.video_details, name='video_details'),
    path('download/<uuid:uuid>/', views.ProtectedMediaView.as_view(), name='video_download'),
    path('stream/<uuid:uuid>/', views.VideoStreamView.as_view(), name='video_stream'),
    path('', views.VideoListView, name='video_list'),

]
