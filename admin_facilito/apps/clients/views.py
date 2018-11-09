from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, FormUser

url_redirect = 'clients:login'

@login_required(login_url=url_redirect)
def view(request):
    return render(request, 'dashboard.html', {})


def login_view(request):
    message = None

    if request.user.is_authenticated():
        return redirect('clients:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return redirect('clients:dashboard')
            else:
                message = 'User or password are incerrect'

    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'message': message})


@login_required(login_url=url_redirect)
def logout_view(request):
    logout(request)
    return redirect('clients:login')


def create(request):
    form = FormUser()

    if request.method == 'POST':
        form = FormUser(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('clients:login')

    return render(request, 'create.html', {'form': form})