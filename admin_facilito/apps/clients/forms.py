from django import forms
from django.contrib.auth.models import User


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

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class EditUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length = 20,
        widget = forms.TextInput(attrs={'class': 'form-control'}),
        error_messages = user_error_messages
    )
    email = forms.CharField(
        widget = forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages = email_error_messages
    )
    first_name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control'}),
    )

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