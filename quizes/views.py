from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return context


class QuestionListView(ListView):
    model = Question
    template_name = 'quizes/question_list.html'