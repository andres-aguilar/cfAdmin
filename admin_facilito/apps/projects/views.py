from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from apps.status.models import Status
from apps.status.forms import StatusChoiceForm

from django.db import transaction

from .forms import ProjectForm, PermissionProject
from .models import Project, ProjectUser, ProjectPermission


class CreateProjectView(LoginRequiredMixin, CreateView):
    """ Create project """
    login_url = 'clients:login'
    template_name = 'projects/create.html'
    model = Project
    form_class = ProjectForm

    def get_url_project(self):
        return reverse_lazy('projects:show', kwargs={'slug': self.object.slug})

    @transaction.atomic
    def create_objects(self):
        self.object.save()
        # Asiganando un estatus al proyecto
        self.object.projectstatus_set.create(status=Status.get_default_status())
        # Asignando los permisos de fundador al usuario creador del proyecto
        self.object.projectuser_set.create(user=self.request.user, 
            permission=ProjectPermission.founder_permission() )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.create_objects()
        return HttpResponseRedirect(self.get_url_project())


class ListUserProjectsView(LoginRequiredMixin, ListView):
    """ List projects """
    login_url = 'clients:login'
    template_name = 'projects/projects.html'

    def get_queryset(self):
        return ProjectUser.objects.filter(user = self.request.user)


class ShowProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/details.html'

    def get_context_data(self, **kwargs):
        context = super(ShowProjectView, self).get_context_data(**kwargs)

        context['has_permission'] = self.object.user_has_permission(self.request.user)

        return context


class ListAllProjectsView(LoginRequiredMixin, ListView):
    """ List projects """
    login_url = 'clients:login'
    template_name = 'projects/all.html'

    def get_queryset(self):
        return Project.objects.all()


class ListContributors(LoginRequiredMixin, ListView):
    template_name = 'projects/contributors.html'

    def get_queryset(self):
        self.project = get_object_or_404(Project, slug=self.kwargs['slug'])
        return ProjectUser.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super(ListContributors, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context


# Functions
def admin_only(function):
    def wrap(request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])

        if not project.user_has_permission(request.user):
            lazy = reverse_lazy('projects:show', kwargs={'slug': project.slug})
            return HttpResponseRedirect(lazy)
        return function(request, *args, **kwargs)
    return wrap


@login_required(login_url='clients:login')
@admin_only
def delete_contributor(request, slug, username):
    project = get_object_or_404(Project, slug=slug)
    user = get_object_or_404(User, username=username)

    projectuser = get_object_or_404(ProjectUser, user=user, project=project)

    if not projectuser.is_founder():
        projectuser.delete()

    return redirect('projects:contributors', slug=project.slug)


@login_required(login_url='clients:login')
def user_contributor(request, slug, username):
    project = get_object_or_404(Project, slug=slug)
    user = get_object_or_404(User, username=username)
    has_permission = project.user_has_permission(request.user)
    permission = get_object_or_404(ProjectUser, user=user, project=project)

    form = PermissionProject(request.POST or None, initial={'permission': permission.permission_id})

    if request.method == 'POST' and form.is_valid():
        selection_id = form.cleaned_data.get('permission').id 

        if selection_id != permission.id and permission.valid_change_permission():
            permission.permission_id = selection_id
            permission.save()
            messages.success(request, 'Datos actualizados correctamente!')

    context = {
        'project': project,
        'user': user,
        'form': form,
        'has_permission': has_permission
    }

    return render(request, 'projects/contributor.html', context)

@login_required(login_url='clients:login')
@admin_only
def add_contributor(request, slug, username):
    project = get_object_or_404(Project, slug=slug)
    user = get_object_or_404(User, username=username)

    if not project.projectuser_set.filter(user=user).exists():
        project.projectuser_set.create(user=user, 
            permission=ProjectPermission.contributor_permission())

    
    return redirect('projects:contributors', slug=project.slug)


@login_required(login_url='clients:login')
@admin_only
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
            status = form_status.cleaned_data.get('status')
            form.save()
            
            if status.id != project.get_id_status():
                project.projectstatus_set.create(status_id=status.id)
                messages.success(request, 'Proyecto actualizado correctamente')

    return render(request, 'projects/edit.html', context)
