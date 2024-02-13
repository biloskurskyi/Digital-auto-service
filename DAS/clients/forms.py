from datetime import date

from django import forms
from django.core.validators import MaxValueValidator

from clients.models import Client


class CreateClientForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter last name'}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter email'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter phone number'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control py-4'}),
        validators=[MaxValueValidator(limit_value=date.today)]
    )
    info = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter something about client'}))

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
