from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.views.generic import View, DetailView, CreateView, UpdateView 

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Client, SocialNetwork
from .forms import LoginForm, CreateUserForm, EditUserForm, EditPasswordForm, EditClientForm, SocialMediaForm


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


    return render(request, 'clients/edit_password.html', {'form': form, 'message': message})


class LoginView(View):
    form = LoginForm()
    message = None 
    template = 'clients/login.html'

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
    template_name = 'clients/show.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class DashboardView(LoginRequiredMixin, View):
    login_url = 'clients:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'clients/dashboard.html', {})


class CreateUserView(CreateView):
    success_url = reverse_lazy('clients:login')
    template_name = 'clients/create.html'
    model = User
    form_class = CreateUserForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """  Edit user view (unused) """
    model = User
    login_url = 'clients:login'
    template_name = 'clients/edit.html'
    success_url = reverse_lazy('clients:edit')
    form_class = EditUserForm
    success_message = 'Tu perfil se ha actualizado correctamente'

    def get_object(self, queryset=None):
        return self.request.user


@login_required(login_url='clients:login')
def edit_client(request):
    client_form = EditClientForm(request.POST or None, instance=user_client(request.user))
    user_form = EditUserForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if client_form.is_valid() and user_form.is_valid():
            user_form.save()
            client_form.save()
            messages.success(request, 'Datos actualizados correctamente')

    return render(request, 'clients/edit_client.html', {'client_form': client_form, 'user_form': user_form})


def user_client(user):
    try:
        return user.client
    except:
        return Client(user=user)


class EditSocialMediaView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'clients:login'
    model = SocialNetwork
    template_name = 'clients/edit_social_network.html'
    success_url = reverse_lazy('clients:edit_social')
    form_class = SocialMediaForm
    success_message = 'Información actualizada correctamente'

    def get_object(self, queryset=None):
        return self.get_social_instance()

    def get_social_instance(self):
        try:
            return self.request.user.socialnetwork
        except:
            return SocialNetwork(user=self.request.user) 

