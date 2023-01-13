from django.shortcuts import render, get_object_or_404, redirect
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

def MyQuizView(request, pk=None):
    # print(request.GET.get('start'), type(request.GET.get('start')))
    quiz = None
    quiz_difficulty = '1'
    # if request.GET.get('start') == 'True' and request.session.get('quiz_completed', True):
    if request.GET.get('start') == 'True':
        questions = Question.objects.filter(id__in=SelectQuestion(quiz_difficulty))
        
        quiz = Quiz.objects.create(
            difficulty=quiz_difficulty,        
        )
        quiz.questions.add(*questions)
        request.session['quiz_id'] = str(quiz.pk)
        request.session['quiz_completed'] = False
        print('quiz created', quiz.pk)
        return redirect ('quizes:my_quiz_proccess', quiz.pk)
    
    # elif not request.session.get('quiz_completed'):
    #     quiz = get_object_or_404(Quiz, pk=request.session.get('quiz_id', None))
    #     print('quiz created before')
    #     return redirect ('quizes:my_quiz_proccess', quiz.pk)
        
    return render(
        request,
        'quizes/my_quiz.html',
        {
            'page_title': _('My quiz'),
            'quiz': quiz ,
        }
    )


def MyQuizProccessView(request, pk):
    print('quiz proccess started', pk)
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()

    # if request.GET.get('q') == 1 :
    question = questions[0]    
    print('question 1: ', question.description, question.correct)
    
    step = int(request.GET.get('q'))
    if not step:
        step = 1
    
    print(request.GET.get('q'), ': q')
    if request.GET.get(question.correct) == 'on': 

        print('correct')
        step += 1

    if step == 2 or request.GET.get('q') == 2 :
        question = questions[1]
        print('question 2: ', question.description, question.correct)
        
    if step == 3 or request.GET.get('q') == 3 :
        question = questions[2]
        print('question 3: ', question.description, question.correct)
        
    if step == 4 or request.GET.get('q') == 4 :
        question = questions[3]
        print('question 4: ', question.description, question.correct)
        
    if step == 5 or request.GET.get('q') == 5 :
        question = questions[4]
        print('question 5: ', question.description, question.correct)
 
    
    next_step = step + 1

    return render(
        request,
        'quizes/my_quiz_proccess.html',
        {
            'page_title': _('My quiz'),
            'quiz': quiz,
            'question': question,
            'step': step, 
            'next_step': next_step, 
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