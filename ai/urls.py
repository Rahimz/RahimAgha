from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('test/', views.AiView, name='ai'),
    path('<str:chat_id>/', views.AiCreateNewChatView, name='ai_continue_chat'),
    path('', views.AiCreateNewChatView, name='ai_create'),
]
