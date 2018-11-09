from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm

# Create your views here.
def view(request):
    return render(request, 'dashboard.html', {})


def login_view(request):
    message = None

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


def logout_view(request):
    logout(request)
    return redirect('clients:login')