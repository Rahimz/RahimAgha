from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
import random 

from django.forms import Select

from .models import Question, Quiz

class QuestionCreateView(CreateView):
    model = Question
    template_name = 'quizes/question_create.html'
    fields = [
        'description', 'correct', 'wrong_1', 'wrong_2', 'wrong_3',
        'difficulty',         
    ]
    success_url = '/quizes/questions/list/'
    

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Create question')
        context['mainNavSection'] = 'quizes' 
        return context


class QuestionListView(ListView):
    model = Question
    template_name = 'quizes/question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Questions list')
        context['mainNavSection'] = 'quizes' 
        return context

def MyQuizView(request):
    # print(request.GET.get('start'), type(request.GET.get('start')))
    if request.GET.get('start') == 'True' and request.session.get('quiz_completed', True):
        questions = SelectQuestion('3')
        # quiz = Quiz.objects.crreate(
        #     difficulty='1',
        #     questions=questions
        # )
        print(questions)

    
        
    return render(
        request,
        'quizes/my_quiz.html',
        {
            'page_title': _('My quiz'),
        }
    )


def SelectQuestion(level):
    """
    This function makes a list of 5 questions id
    and returns it in a list
    """
    qs_easy = list(Question.objects.filter(difficulty__in=['1']).values_list('pk', flat=True))
    qs_medium = list(Question.objects.filter(difficulty__in=['2', '3']).values_list('pk', flat=True))
    qs_hard = list(Question.objects.filter(difficulty__in=['4', '5']).values_list('pk', flat=True))

    if level == '1':
        questions = random.sample(qs_easy, 1) + random.sample(qs_medium, 3) + random.sample(qs_hard, 1)
    if level == '2':
        questions = random.sample(qs_easy, 1) + random.sample(qs_medium, 2) + random.sample(qs_hard, 2)
    if level == '3':
        questions = random.sample(qs_easy, 1) + random.sample(qs_medium, 1) + random.sample(qs_hard, 3)
    return questions


def QuizResultView(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if not quiz.completed:
        quiz = None
    
    return render(
        request,
        'quiz/question_list.html',
        {
            'quiz': quiz,
            'page_title': _('Quiz results')
        }
    )