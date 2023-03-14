from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'quizes'

urlpatterns = [
    path('questions/create/', login_required(views.QuestionCreateView.as_view()), name='question_create' ),
    path('questions/update/<int:pk>/', login_required(views.QuestionUpdateView.as_view()), name='question_update' ),
    path('questions/list/', login_required(views.QuestionListView.as_view()), name='questions_list' ),
    
    path('compliment/create/', login_required(views.ComplimentCreateView.as_view()), name='compliment_create' ),
    path('compliment/update/<int:pk>/', login_required(views.ComplimentUpdateView.as_view()), name='compliment_update' ),
    path('compliment/list/', login_required(views.ComplimentListView.as_view()), name='compliment_list' ),

    path('my-quiz/result/<uuid:pk>/', views.QuizResultView, name='my_quiz_result' ),    
    path('my-quiz/<str:error>/<uuid:quiz_pk>/<int:step>/', views.NewMyQuizProccessView, name='my_quiz_proccess_error' ),
    path('my-quiz/<uuid:quiz_pk>/<int:step>/', views.NewMyQuizProccessView, name='my_quiz_proccess' ),
    path('my-quiz/', views.MyQuizView, name='my_quiz' ), #also uses for start a quiz

    # reports
    path('questions/update-report/', views.QuestionCorrectRateUpdate, name="update_question_report"),

]
