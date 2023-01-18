from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
import random 

from django.forms import Select

from .models import Question, Quiz, QuizResponse

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
        questions_id = SelectQuestion(quiz_difficulty)
        questions = Question.objects.filter(id__in=questions_id)
        
        quiz = Quiz.objects.create(
            difficulty=quiz_difficulty,
            questions_id = questions_id,
        )
        quiz.questions.add(*questions)

        # make QuizResponse for every single question
        for item in questions:
            quizRespone = QuizResponse.objects.create(
                quiz = quiz,
                question = item,
                answers = item.get_answers(),
                correct_answer = item.correct,
            )

        return redirect ('quizes:my_quiz_proccess', quiz.pk, 1)
    

        
    return render(
        request,
        'quizes/my_quiz.html',
        {
            'page_title': _('My quiz'),
            'quiz': quiz ,
        }
    )

def NewMyQuizProccessView(request, quiz_pk, step=1):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    responses = quiz.responses.all()
    print('responses is created', responses.count())
    response = responses[step-1]
    question = response.question
    answers = response.answers
    if request.method == 'POST':
        user_answer = None
        answer_list = response.answers 
        for item in '1234':
            # print(f"{item}: ", request.POST.get(f"answer-{item}"))
            if request.POST.get(f"answer-{item}") == 'on':
                user_answer = f"answer-{item}"
                user_answer_string = response.answers[int(item) - 1]
        
        #  we wan to write user response to the record
        response.user_response = user_answer_string
        response.save()
        # print('user respnse saved', response.user_response)
        # print(f'user response for step {step} stores to quizResponse')
        if step <= 4:
            return redirect('quizes:my_quiz_proccess', quiz_pk, step + 1)
        else:
            return redirect ('quizes:my_quiz_result', quiz.pk)

    return render(
        request,
        'quizes/my_quiz_proccess.html',
        {
            'page_title': _('My quiz'),
            'quiz': quiz,
            'question': question,
            'answers': answers,
            'step': step, 
            # 'next_step': next_step, 
        }
    )


def QuizResultView(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    responses = quiz.responses.all()


    
    return render(
        request,
        'quizes/show_results.html',
        {
            'quiz': quiz,
            'page_title': _('Quiz results'),
            'responses': responses,
        }
    )

def MyQuizProccessView(request, pk, step=1):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()
    user_answer = None
   
    if request.method == 'POST':
        for item in '1234':
            # print(f"{item}: ", request.POST.get(f"answer-{item}"))
            if request.POST.get(f"answer-{item}") == 'on':
                user_answer = f"answer-{item}"
        print(f'check {step} question ')
        question = questions[step-1]
        request.session[str(question.id)]['response'] = user_answer
        print(f'write {step} answer in session', user_answer)
        

        step = step + 1
        question = questions[step-1]
        answers = question.get_answers()
        request.session[str(question.id)] = {'answers': answers, 'response': None}
        print(f'prepare {step} question')

        if step > 4:
            print(f'if {step} >4 answer in session and redirect')
            request.session[str(questions[4].id)]['response'] = user_answer
            # print(user_answer)
            return redirect ('quizes:my_quiz_result', quiz.pk)


        

        return redirect ('quizes:my_quiz_proccess', quiz.pk, step)

    
    # make first question 
    print(f'prepare {step} question')
    question = questions[step-1]
    answers = question.get_answers()
    request.session[str(question.id)] = {'answers': answers, 'response': None}
   

    return render(
        request,
        'quizes/my_quiz_proccess.html',
        {
            'page_title': _('My quiz'),
            'quiz': quiz,
            'question': question,
            'answers': answers,
            'step': step, 
            # 'next_step': next_step, 
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


