import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Project


class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Título',
        required = True,
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label = 'Descripción',
        required = True,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    dead_line = forms.DateField(
        initial = datetime.date.today,
        widget = forms.DateInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Project
        fields = ('title', 'description', 'dead_line')