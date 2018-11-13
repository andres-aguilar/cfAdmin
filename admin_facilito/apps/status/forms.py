from django import forms

from .models import Status

class StatusChoiceForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset = Status.objects.all(),
        initial = 0,
        widget =  forms.Select(attrs={'class': 'form-control'})
    )