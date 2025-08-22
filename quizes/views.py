from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
# from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
import random 
import requests
from PIL import Image as IMG
from io import BytesIO
from django.core.files import File
from django.contrib.admin.views.decorators import staff_member_required
from bs4 import BeautifulSoup


from .models import Question, Quiz, QuizResponse, Compliment

# staff access
class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'quizes/question_create.html'
    fields = [
        'description', 'correct', 'wrong_1', 'wrong_2', 'wrong_3',
        'difficulty', 'link', 'published' 
    ]
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('generals:no_access')
        return super().dispatch(request, *args, **kwargs)

    # success_url = '/quizes/questions/list/'
    def get_success_url(self):
        return reverse ('quizes:questions_list')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Create question')
        context['mainNavSection'] = 'quizes' 
        return context


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'quizes/question_create.html'
    fields = [
        'description', 'correct', 'wrong_1', 'wrong_2', 'wrong_3',
        'difficulty', 'link', 'published'           
    ]
    # superuser access
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('generals:no_access')
        return super().dispatch(request, *args, **kwargs)
    
    # success_url = '/quizes/questions/list/'
    def get_success_url(self):
        return reverse ('quizes:questions_list')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Update question')
        context['mainNavSection'] = 'quizes' 
        return context


class QuestionListView(LoginRequiredMixin, ListView):
    queryset = Question.objects.all()
    model = Question
    template_name = 'quizes/question_list.html'
    ordering = ('difficulty', )

    # superuser access
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('generals:no_access')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.GET.get('search'):

            return super().get_queryset().annotate(
            search=SearchVector('description', 'correct', 'wrong_1', 'wrong_2', 'wrong_3'),
                ).filter(search=self.request.GET.get('search'))

        return super().get_queryset()
       
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Questions list')
        context['mainNavSection'] = 'quizes'
        if self.request.GET.get('search'):
            context['query'] = self.request.GET.get('search')
   
        return context

def MyQuizView(request, pk=None):
    # print(request.GET.get('start'), type(request.GET.get('start')))
    quiz = None

    #  set the quiz difficulty
    quiz_difficulty = '1'
    if request.GET.get('diff') == '2':
        quiz_difficulty = '2'
    elif request.GET.get('diff') == '3':
        quiz_difficulty = '3'

    # if request.GET.get('start') == 'True' and request.session.get('quiz_completed', True):
    if request.GET.get('start') == 'True':
        questions_id = SelectQuestion(quiz_difficulty)
        questions = Question.objects.filter(id__in=questions_id)
        
        # if any old and unfinished quiz be in the session it should be finished first
        old_quiz_id = request.session.get('quiz_id', None)
        old_quiz = None
        if old_quiz_id:
            try:
                old_quiz = Quiz.objects.get(pk=old_quiz_id)
            except:
                pass
        
        if old_quiz:
            if not old_quiz.completed:
                return redirect('quizes:my_quiz_proccess', old_quiz.pk, 1)

        # create quiz
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        quiz = Quiz.objects.create(
            difficulty=quiz_difficulty,
            questions_id = questions_id,
            ip = ip,
        )
        quiz.questions.add(*questions)

        request.session['quiz_id'] = str(quiz.pk)
        # print(request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip())
        # make QuizResponse for every single question
        temp_step = 1
        for item in questions_id:
            question = Question.objects.get(pk=item)
            quizRespone = QuizResponse.objects.create(
                quiz = quiz,
                question = question,
                answers = question.get_answers(),
                correct_answer = question.correct,
                step=temp_step
            )
            temp_step += 1

        return redirect ('quizes:my_quiz_proccess', quiz.pk, 1)
    

        
    return render(
        request,
        'quizes/my_quiz.html',
        {
            'page_title': _('My quiz'),
            'quiz': quiz ,
        }
    )


def NewMyQuizProccessView(request, quiz_pk, step=1, error=None):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    # check if the quiz completed or not
    if quiz.completed:
        return redirect('quizes:my_quiz_result', quiz_pk)
    #  the responses order by the step
    responses = quiz.responses.all().order_by('step')
    #  we always select the first step from the remaining steps
    remain_step = list(responses.filter(done=False).values_list('step', flat=True))
    if len(remain_step) > 0:
        current_step = remain_step[0]
    else:       
        return redirect('quizes:my_quiz_result', quiz_pk)
    
    required_msg = None

    if error == 'error':
        required_msg =  _('Please choose one')


    # print('responses is created', responses.count())
    response = responses.get(step=current_step)
    question = response.question
    answers = response.answers
    if request.method == 'POST':
        # user_answer = None
        # answer_list = response.answers 
        user_answer_string = request.POST.get('answer')
        # multiple = 0
        # print(request.POST.get('answer'))
        # for item in '1234':
        #     # print(f"{item}: ", request.POST.get(f"answer-{item}"))
        #     if request.POST.get(f"answer-{item}") == 'on':
        #         user_answer = f"answer-{item}"
        #         user_answer_string = response.answers[int(item) - 1]
        #         multiple += 1
        
        # if multiple > 1:
        #     return redirect ('quizes:my_quiz_proccess_error', 'error', quiz_pk, current_step)
        # if not user_answer_string:
        #     return redirect ('quizes:my_quiz_proccess_error', 'error', quiz_pk, current_step)
        #  we want to write user response to the record
        response.user_response = user_answer_string
        response.done = True
        response.save()
        # print('user respnse saved', response.user_response)
        # print(f'user response for step {step} stores to quizResponse')
        if step <= 4:
            return redirect('quizes:my_quiz_proccess', quiz_pk, current_step + 1)
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
            'required_msg': required_msg,
           
        }
    )


def QuizResultView(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    responses = quiz.responses.all().order_by('step')

    responses_dict = {}

    sum = 0
    for response in responses:
        src = None
        # if response.question.link:
        #     try:
        #         res = requests.get(response.question.link)
        #     except:
        #         res = None
        #     if res:
        #         soup = BeautifulSoup(res.text, 'html.parser')
        #         src = f"https://ketabedamavand.com{soup.body.main.img['src']}"
        if not response.question.image:
            src = GrabBookData(response)
        responses_dict[response.id] = {
            'question': response.question,
            'result': response.result,
            # 'book_link': response.question.link,
            'src': src, 
            # 'image': response.question.image.url,
            'correct': response.correct_answer, 
            'user_response': response.user_response, 
        }
  
        if response.result:
            sum += 1
    
    quiz.final_result = sum 
    quiz.completed = True
    quiz.save(update_fields=['final_result', 'completed'])
    request.session['quiz_id'] = None

    compliment_qs = list(Compliment.objects.filter(difficulty=sum).values_list('content', flat=True))
    compliment = random.sample(compliment_qs, 1)
    if len(compliment) > 0:
        compliment = compliment[0]
    return render(
        request,
        'quizes/show_results.html',
        {
            'quiz': quiz,
            'page_title': _('Quiz results'),
            'responses': responses,
            'responses_dict': responses_dict,
            'sum': sum, 
            'compliment': compliment, 
        }
    )


def GrabBookData(response):
    src = None
    if response.question.link:
        question = response.question
        try:
            res = requests.get(response.question.link)
        except:
            res = None
        if res:
            soup = BeautifulSoup(res.text, 'html.parser')
            src = f"https://ketabedamavand.com{soup.body.main.img['src']}"
            if 'no_image.png' in src:
                src = None

    if src:
        im = IMG.open(requests.get(src, stream=True).raw)
        extension = src.split('.')[-1]
        if extension in ('jpg', 'jpeg'):
            ext = 'JPEG'
        elif extension in ('png', 'PNG'):
            ext = 'PNG'
        elif extension in ('webp', 'WEBP'):
            ext = 'WEBP'
        else:
            ext = None
        
        if ext:
            try:
                blob = BytesIO()
                im.save(blob, ext) 

                question.image.save(f"test.{extension}", File(blob), save=True)
            except:
                pass
    return src


def SelectQuestion(level):
    """
    This function makes a list of 5 questions id
    and returns it in a list
    """
    questions_qs = Question.get_published.all()
    qs_easy = list(questions_qs.filter(difficulty__in=['1']).values_list('pk', flat=True))
    qs_medium = list(questions_qs.filter(difficulty__in=['2', '3']).values_list('pk', flat=True))
    qs_hard = list(questions_qs.filter(difficulty__in=['4', '5']).values_list('pk', flat=True))

    if level == '1':
        questions = random.sample(qs_easy, 1) + random.sample(qs_medium, 3) + random.sample(qs_hard, 1)
    if level == '2':
        questions = random.sample(qs_easy, 1) + random.sample(qs_medium, 2) + random.sample(qs_hard, 2)
    if level == '3':
        questions = random.sample(qs_easy, 1) + random.sample(qs_medium, 1) + random.sample(qs_hard, 3)
    return questions


class ComplimentCreateView(LoginRequiredMixin, CreateView):
    model = Compliment
    template_name = 'quizes/question_create.html'
    fields = [
        'content', 'difficulty'
    ]
    
    # superuser access
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('generals:no_access')
        return super().dispatch(request, *args, **kwargs)
    
    # success_url = '/quizes/questions/list/'
    def get_success_url(self):
        return reverse ('quizes:compliment_list')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Create compliment')
        context['mainNavSection'] = 'quizes' 
        return context


class ComplimentUpdateView(LoginRequiredMixin, UpdateView):
    model = Compliment
    template_name = 'quizes/question_create.html'
    fields = [
        'content', 'difficulty'        
    ]
    # superuser access
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('generals:no_access')
        return super().dispatch(request, *args, **kwargs)
    
    # success_url = '/quizes/questions/list/'
    def get_success_url(self):
        return reverse ('quizes:compliment_list')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Update compliment')
        context['mainNavSection'] = 'quizes' 
        return context


class ComplimentListView(LoginRequiredMixin, ListView):
    queryset = Compliment.objects.all()
    model = Compliment
    template_name = 'quizes/question_list.html'
    ordering = ('difficulty', )

    
    # superuser access
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('generals:no_access')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.GET.get('search'):

            return super().get_queryset().annotate(
            search=SearchVector('content'),
                ).filter(search=self.request.GET.get('search'))

        return super().get_queryset()
       
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Compliment list')
        context['mainNavSection'] = 'quizes'
        context['compliment'] = True
        if self.request.GET.get('search'):
            context['query'] = self.request.GET.get('search')
   
        return context
    

# @staff_member_required
@login_required
def QuestionCorrectRateUpdate(request):
    if not request.user.is_superuser:
        return redirect('generals:no_access')
    questions = Question.objects.all()
    for item in questions.iterator():
        uses = item.question_uses.all().count()
        corrects = item.question_uses.filter(result=True).count()
        no_responses = uses - corrects
        item.uses = uses
        item.correct_responses = corrects
        item.no_response = no_responses
        item.save()
        print(uses, corrects, no_responses, item.get_correct_percent)
    return redirect('quizes:questions_list')