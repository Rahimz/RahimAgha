from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from .views import RegisterView
# from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('register/', views.register, name='register'),
]