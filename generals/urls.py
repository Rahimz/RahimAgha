from django.urls import path
from . import views

app_name = "generals"

urlpatterns = [
    path('geolocation/<str:ip>/', views.GetCountryFromIP.as_view(), name="geo"),
    path('no-access/', views.NoAccessView, name='no_access'),
    path('', views.HomeView, name='home'),
]
