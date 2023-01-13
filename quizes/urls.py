from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'quizes'

urlpatterns = [
    path('questions/create/', login_required(views.QuestionCreateView.as_view()), name='question_create' ),
    path('questions/list/', login_required(views.QuestionListView.as_view()), name='questions_list' ),

    path('my-quiz/result/<uuid:pk>/', views.QuizResultView, name='my_quiz_result' ),    
    path('my-quiz/<uuid:pk>/', views.MyQuizProccessView, name='my_quiz_proccess' ),
    path('my-quiz/', views.MyQuizView, name='my_quiz' ), #also uses for start a quiz
]
