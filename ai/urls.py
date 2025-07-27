from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('create/', views.AiCreateNewChatView, name='ai_create'),
    path('continue/<str:chat_id>/', views.AiCreateNewChatView, name='ai_continue_chat'),
    path('', views.AiView, name='ai'),
]
