from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('geolocation/<str:ip>/', views.GetCountryFromIP.as_view(), name="geo")
]
