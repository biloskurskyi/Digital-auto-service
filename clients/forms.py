from django import forms

from core.forms import StyledForm

from .models import Client


class ClientForm(StyledForm, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'info')
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}
