from django import forms

from clients.models import Client
from core.forms import StyledForm

from .models import Car


class CarForm(StyledForm, forms.ModelForm):
    class Meta:
        model = Car
        fields = ('client', 'car_number', 'vin_number', 'mark', 'model', 'year', 'engine', 'gear_type', 'comment')
        widgets = {'comment': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, tenant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.for_tenant(tenant)
        self.fields['client'].empty_label = None
