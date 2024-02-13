from django import forms

from cars.models import Car
from stations.models import Station

from .models import Order
from django.db.models import Q


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        manager = kwargs.pop('manager', None)
        stations = kwargs.pop('stations', None)

        super(CreateOrderForm, self).__init__(*args, **kwargs)

        if owner:
            self.fields['client'].queryset = owner.client_set.all()
        if manager:
            owner = manager.owner if manager.owner else manager
            self.fields['client'].queryset = owner.client_set.all()

        self.fields['car'].queryset = Car.objects.none()
        self.fields['service_station'].queryset = Station.objects.none()

        if owner:
            self.fields['service_station'].queryset = Station.objects.filter(
                Q(owner=owner) | Q(owner__owner=owner)
            )
        elif manager:
            self.fields['service_station'].queryset = stations.filter(
                Q(owner=manager) | Q(owner__owner=manager)
            )

        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                self.fields['car'].queryset = Car.objects.filter(client_id=client_id)
            except (ValueError, TypeError):
                pass
        elif self.instance and hasattr(self.instance, 'client') and self.instance.client:
            self.fields['car'].queryset = self.instance.client.car_set.all()

        # print(stations)
        # if True:
        #     self.fields['service_station'].queryset = stations
        #     print(stations)


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'car', 'start_date', 'process_status', 'info', 'service_station')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        manager = kwargs.pop('manager', None)
        stations = kwargs.pop('stations', None)

        super(UpdateOrderForm, self).__init__(*args, **kwargs)
        if owner:
            self.fields['client'].queryset = owner.client_set.all()
        if manager:
            owner = manager.owner if manager.owner else manager
            self.fields['client'].queryset = owner.client_set.all()

        self.fields['client'].disabled = True
        self.fields['car'].disabled = True
        if owner:
            self.fields['service_station'].queryset = Station.objects.filter(
                Q(owner=owner) | Q(owner__owner=owner)
            )
        elif manager:
            self.fields['service_station'].queryset = stations.filter(
                Q(owner=manager) | Q(owner__owner=manager)
            )
