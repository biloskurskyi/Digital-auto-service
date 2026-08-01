from django import forms

from cars.models import Car
from clients.models import Client
from core.forms import StyledForm
from stations.models import Station
from workers.models import Worker

from .models import Order


class OrderForm(StyledForm, forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.none(), required=False, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Order
        fields = ('client', 'car', 'start_date', 'process_status', 'info', 'station')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'info': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, tenant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.for_tenant(tenant)
        self.fields['station'].queryset = Station.objects.for_tenant(tenant)
        self.fields['workers'].queryset = Worker.objects.for_tenant(tenant)
        if self.instance.pk:
            self.fields['client'].disabled = True
            self.fields['car'].disabled = True
            self.fields['car'].queryset = self.instance.client.car_set.all()
            self.fields['workers'].initial = self.instance.workers.all()
        else:
            self.fields['car'].queryset = self.posted_client_cars(tenant)

    def posted_client_cars(self, tenant):
        try:
            client_id = int(self.data.get('client'))
        except (TypeError, ValueError):
            return Car.objects.none()
        return Car.objects.for_tenant(tenant).filter(client_id=client_id)
