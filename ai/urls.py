from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('', views.AiView, name='ai')
]
