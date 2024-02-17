from datetime import date

from django import forms
from django.core.validators import MaxValueValidator

from orders.models import Order
from .models import Worker


class WorkerForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter last name'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control py-4'}),
        validators=[MaxValueValidator(limit_value=date.today)]
    )
    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter years of experience'}))
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter skills'}))
    salary = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter Salary'}))
    orders = forms.ModelMultipleChoiceField(
        queryset=Order.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select'}),
        required=False,  # If you want orders to be optional
    )

    class Meta:
        model = Worker
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'orders': forms.CheckboxSelectMultiple(),  # Using checkboxes for multiple selection of orders
        }
