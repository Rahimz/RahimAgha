from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('details/<uuid:uuid>/', views.video_details, name='video_details'),
    path('download/<uuid:uuid>/', views.ProtectedMediaView.as_view(), name='video_download'),
    path('stream/<uuid:uuid>/', views.VideoStreamView.as_view(), name='video_stream'),
    path('stream-atman/<uuid:uuid>/', views.AtmanVideoStreamView.as_view(), name='video_stream_atman'),
    path('upload/', views.FileUploader.as_view(), name='file_upload'), 
    path('new-upload/', views.NewFileUploader, name='new_file_upload'), 

    path('add-category/', views.AddCategoryView, name='add_category'),
    path('category/<int:category_id>/', views.VideoListView, name='category_view'),

    path('', views.VideoListView, name='video_list'),
]
