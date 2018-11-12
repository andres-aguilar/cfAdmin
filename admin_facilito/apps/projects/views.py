from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Project
from .forms import ProjectForm

class CreateProjectView(LoginRequiredMixin, CreateView):
    login_url = 'clients:login'
    template_name = 'projects/create.html'
    model = Project
    form_class = ProjectForm
