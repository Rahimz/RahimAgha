from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'quizes'

urlpatterns = [
    path('questions/create/', login_required(views.QuestionCreateView.as_view()), name='question_create' ),
    path('questions/list/', login_required(views.QuestionListView.as_view()), name='questions_list' ),

    path('my-quiz/', views.MyQuizView, name='my_quiz' ), #also uses for start a quiz
    
    path('my-quiz/<uuid:pk>/', views.MyQuizView, name='My_quiz_proccess' ),
    path('my-quiz/result/<uuid:pk>/', views.QuizResultView, name='My_quiz_result' ),
]
