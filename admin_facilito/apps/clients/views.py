from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect

from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.views.generic import View, DetailView, CreateView, UpdateView 
from django.contrib.messages.views import SuccessMessageMixin

from .forms import LoginForm, CreateUserForm, EditUserForm, EditPasswordForm


@login_required(login_url='clients:login')
def logout_view(request):
    logout(request)
    return redirect('clients:login')

@login_required(login_url='clients:login')
def edit_password(request):
    form = EditPasswordForm(request.POST or None)
    message = None

    if request.method == 'POST':
        if form.is_valid():
            current_pass = form.cleaned_data.get('password')
            new_pass = form.cleaned_data.get('new_password')

            if authenticate(username=request.user.username, password=current_pass):
                request.user.set_password(new_pass)
                request.user.save()
                update_session_auth_hash(request, request.user)
                message = 'password actualizado'


    return render(request, 'edit_password.html', {'form': form, 'message': message})


class LoginView(View):
    form = LoginForm()
    message = None 
    template = 'login.html'

    def get_context(self):
        return {'form': self.form, 'message': self.message}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('clients:dashboard')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return redirect('clients:dashboard')
            else:
                self.message = 'User or password are incerrect'
            return render(request, self.template, self.get_context())


class ShowUserView(DetailView):
    model = User
    template_name = 'show.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class DashboardView(LoginRequiredMixin, View):
    login_url = 'clients:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', {})


class CreateUserView(CreateView):
    success_url = reverse_lazy('clients:login')
    template_name = 'create.html'
    model = User
    form_class = CreateUserForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    login_url = 'clients:login'
    template_name = 'edit.html'
    success_url = reverse_lazy('clients:edit')
    form_class = EditUserForm
    success_message = 'Tu perfil se ha actualizado correctamente'

    def get_object(self, queryset=None):
        return self.request.user
