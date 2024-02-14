from django import forms

from clients.models import Client
from .models import Car


class CreateCarForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    empty_label=None)
    car_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter car number'}))
    vin_number = forms.CharField(max_length=17, widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Enter VIN number'}))
    mark = forms.CharField(max_length=16,
                           widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter mark'}))
    model = forms.CharField(max_length=32,
                            widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter model'}))
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter year'}))
    engine = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Enter engine'}))
    gear_type = forms.ChoiceField(choices=Car.STATUSES, widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter comment'}))

    class Meta:
        model = Car
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        manager = kwargs.pop('manager', None)

        super(CreateCarForm, self).__init__(*args, **kwargs)

        if owner:
            self.fields['client'].queryset = owner.client_set.all()
        if manager:
            owner = manager.owner if manager.owner else manager
            self.fields['client'].queryset = owner.client_set.all()
