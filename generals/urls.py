from django.urls import path
from . import views

app_name = "generals"

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('geolocation/<str:ip>/', views.GetCountryFromIP.as_view(), name="geo"),
    path('no-access/', views.NoAccessView, name='no_access'),
]
