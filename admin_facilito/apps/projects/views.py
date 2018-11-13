from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from apps.status.models import Status
from apps.status.forms import StatusChoiceForm

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
        # Asiganando un estatus al proyecto
        self.object.projectstatus_set.create(status=Status.get_default_status())
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


@login_required(login_url='clients:login')
def edit_project(request, slug=''):
    project = get_object_or_404(Project, slug=slug)
    form = ProjectForm(request.POST or None, instance=project)
    form_status = StatusChoiceForm(request.POST or None, initial={'status': project.get_id_status()})
    context = {
        'form': form,
        'form_status': form_status
    }

    if request.method == 'POST':
        if form.is_valid() and form_status.is_valid():
            form.save()
            status = form_status.cleaned_data.get('status')
            project.projectstatus_set.create(status_id=status.id)
            messages.success(request, 'Proyecto actualizado correctamente')

    return render(request, 'projects/edit.html', context)
