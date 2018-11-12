from django import forms
from django.contrib.auth.models import User

from .models import Client, SocialNetwork

# Comman variables
user_error_messages = {'required' : 'El nombre de usuario es obligatorio', 'unique' : 'El nombre de usuario no está disponible'}
password_error_messages = {'required' : 'La contraseña es obligatoria'}
email_error_messages = {'required' : 'El email es obligatorio', 'invalid' : 'Ingresa un email valido'}

# Validations
def pass_validator(passwd):
    if len(passwd) < 5:
        raise forms.ValidationError('El password debe tener más de 5 caracteres', code='invalid')



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


class CreateUserForm(forms.ModelForm):
    """ Form user class """
    username = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        error_messages = user_error_messages
    )
    password = forms.CharField(
        max_length = 20,
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages = password_error_messages
    )
    email = forms.CharField(
        widget = forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages = email_error_messages
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count():
            raise forms.ValidationError("El email ya está registrado")
        return email

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class EditUserForm(forms.ModelForm):
    username = forms.CharField(
        label = 'Nombre de usuario',
        max_length = 20,
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        error_messages = user_error_messages
    )
    email = forms.CharField(
        widget = forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages = email_error_messages
    )
    first_name = forms.CharField(
        label = 'Nombre',
        widget = forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        label = 'Apellidos',
        widget = forms.TextInput(attrs={'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Excluimos el usuario para evitar comparar contra él mismo
        if User.objects.filter(email=email).exclude(pk=self.instance.id).count():
            raise forms.ValidationError("El email ya está registrado")
        return email

    class Meta:
        model =  User
        fields = ('username', 'email', 'first_name', 'last_name')


class EditPasswordForm(forms.Form):
    password = forms.CharField(
        max_length = 20,
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
        validators = [pass_validator]
    )
    new_password = forms.CharField(
        max_length = 20,
        widget = forms.PasswordInput(attrs={'class': 'form-control'},),
        validators = [pass_validator]
    )
    repeat_new_password = forms.CharField(
        max_length = 20,
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
        validators = [pass_validator]
    )

    def clean(self):
        clean_data = super(EditPasswordForm, self).clean()
        password1 = clean_data.get('new_password')
        password2 = clean_data.get('repeat_new_password')

        if password1 != password2:
            raise forms.ValidationError('Los password no son los mismos', code='invalid')


class EditClientForm(forms.ModelForm):
    job = forms.CharField(
        label = 'Trabajo actual',
        max_length = 100,
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        label = 'Biografía',
        max_length = 200,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Client
        exclude = ['user']


class SocialMediaForm(forms.ModelForm):
    facebook = forms.URLField(
        max_length = 100,
        widget = forms.URLInput(attrs={'class': 'form-control'})
    )
    twitter = forms.URLField(
        max_length = 100,
        widget = forms.URLInput(attrs={'class': 'form-control'})
    )
    github = forms.URLField(
        max_length = 100,
        widget = forms.URLInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = SocialNetwork
        exclude = ['user']