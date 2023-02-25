from django.urls import path
from . import views

app_name = 'api'


urlpatterns = [
    path('question/list/', views.QuestionListAPIView.as_view(), name='api_question_list' ),
]