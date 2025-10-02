from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('models-list/add/', views.AiModelAddView, name='add_model'),
    path('models-list/', views.AiModelsListView, name='ai_models_list'),
    path('test/', views.AiView, name='ai'),
    path('chats-list/', views.ChatListView, name='ai_chats_list'),
    path('image/new/', views.AiImageView, name='ai_image_new_chat'),      # For new chat
    path('image/<str:chat_id>/', views.AiImageView, name='ai_image_continue_chat'),  # For continuing existing chat
    path('<str:chat_id>/', views.AiCreateNewChatView, name='ai_continue_chat'),
    path('', views.AiCreateNewChatView, name='ai_create'),
]
