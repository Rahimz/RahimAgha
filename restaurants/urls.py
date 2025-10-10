from django.urls import path 
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.ResHomeView, name='res_home'),
    path('review/', views.ReviewView, name='review'),
]
