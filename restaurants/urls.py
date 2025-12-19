from django.urls import path 
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('review/<uuid:place_uuid>/', views.ReviewView, name='review'),
    path('review/vote-view/<uuid:vote_uuid>/', views.VoteDetailsView, name='res_vote_view'),
    path('', views.ResHomeView, name='res_home'),
]
