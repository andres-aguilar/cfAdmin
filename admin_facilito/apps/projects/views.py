from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from .models import Project
from .forms import ProjectForm


class CreateProjectView(LoginRequiredMixin, CreateView):
    """ Create project """
    login_url = 'clients:login'
    template_name = 'projects/create.html'
    model = Project
    form_class = ProjectForm

    def get_url_project(self):
        return reverse_lazy('projects:show', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_url_project())


class ListProjectsView(LoginRequiredMixin, ListView):
    """ List projects """
    login_url = 'clients:login'
    template_name = 'projects/projects.html'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).order_by('dead_line')


class ShowProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/details.html'