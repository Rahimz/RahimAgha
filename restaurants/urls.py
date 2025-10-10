from django.urls import path 
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.ResHomeView, name='res_home'),
    path('review/<uuid:place_uuid>/', views.ReviewView, name='review'),
]
