from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.utils.translation import gettext_lazy as _

from projects.models import ProjectCategory

class ProjectView(ListView):
    
    model = ProjectCategory
    queryset = ProjectCategory.objects.all()
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        # return super().get_queryset().prefetch_related('projects')
        return ProjectCategory.objects.with_details().all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Project")
        
        return context
    
    