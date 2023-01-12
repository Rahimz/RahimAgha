from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'quizes'

urlpatterns = [
    path('questions/create/', login_required(views.QuestionCreateView.as_view()), name='question_create' ),
    path('questions/list/', views.QuestionListView.as_view(), name='questions_list' ),
]
