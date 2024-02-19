from datetime import date

from django import forms
from django.core.validators import MaxValueValidator
from django.db.models import Q

from orders.models import Order
from stations.models import Station
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
        required=False  # If you want orders to be optional
    )

    class Meta:
        model = Worker
        fields = '__all__'
        exclude = ('owner',)
        # widgets = {
        #     'orders': forms.CheckboxSelectMultiple(),  # Using checkboxes for multiple selection of orders
        # }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        manager = kwargs.pop('manager', None)
        orders = kwargs.pop('orders', None)
        super(WorkerForm, self).__init__(*args, **kwargs)

        if owner:
            self.fields['orders'].queryset = Order.objects.filter(
                Q(client__owner=owner)
            )
        elif manager:
            print(manager)
            self.fields['orders'].queryset = Order.objects.filter(
                Q(client__owner=manager.owner.id)
            )
    # def __init__(self, *args, **kwargs):
    #     owner = kwargs.pop('owner', None)
    #     manager = kwargs.pop('manager', None)
    #     orders = kwargs.pop('orders', None)
    #     # print(owner)
    #     super(WorkerForm, self).__init__(*args, **kwargs)
    #
    #     if owner:
    #         self.fields['worker'].queryset = owner.client_set.all()
    #     if manager:
    #         owner = manager.owner if manager.owner else manager
    #         self.fields['client'].queryset = owner.client_set.all()
    #
    #     if owner:
    #         print(owner)
    #         self.fields['orders'].queryset = Order.objects.filter(
    #             Q(client=owner) | Q(client__owner=owner)
    #         )
    #
    #     elif manager:
    #         self.fields['orders'].queryset = orders.filter(
    #             Q(owner=manager) | Q(owner__owner=manager)
    #         )
