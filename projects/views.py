from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class ProjectView(TemplateView):
    template_name = 'projects/projects.html'
    