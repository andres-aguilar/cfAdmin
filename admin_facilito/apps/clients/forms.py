from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    """ LogIn form """
    username = forms.CharField(
        max_length=20,
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=20,
        widget = forms.PasswordInput(attrs={'class': 'form-control'}) 
    )


class FormUser(forms.ModelForm):
    """ Form user class """
    username = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        error_messages = {
            'required' : 'El nombre de usuario es obligatorio',
            'unique' : 'El nombre de usuario no está disponible'
        }
    )
    password = forms.CharField(
        max_length = 20,
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages = {
            'required' : 'La contraseña es obligatoria'
        }
    )
    email = forms.CharField(
        widget = forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages = {
            'required' : 'El email es obligatorio',
            'invalid' : 'Ingresa un email valido'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email')