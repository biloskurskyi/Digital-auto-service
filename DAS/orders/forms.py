from django import forms
from django.db.models import Q
from django.utils import timezone

from cars.models import Car
from clients.models import Client
from stations.models import Station
from workers.models import Worker

from .models import Order


class CreateOrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    empty_label="---")
    car = forms.ModelChoiceField(queryset=Car.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                 empty_label="---")
    start_date = forms.DateField(initial=timezone.now,
                                 widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
    process_status = forms.ChoiceField(choices=Order.STATUSES, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Enter process status'}))
    info = forms.CharField(max_length=200,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control py-4', 'placeholder': 'Enter information'}))
    service_station = forms.ModelChoiceField(queryset=Station.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}),
                                             empty_label=None)
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select'}),
        required=False,  # If you want orders to be optional
    )

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

        if owner:
            self.fields['workers'].queryset = Worker.objects.filter(
                Q(owner=owner)
            )
        elif manager:
            print(manager)
            self.fields['workers'].queryset = Worker.objects.filter(
                Q(owner=manager.owner.id)
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
    client = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                    empty_label="---")
    car = forms.ModelChoiceField(queryset=Car.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                                 empty_label="---")
    start_date = forms.DateField(initial=timezone.now,
                                 widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
    process_status = forms.ChoiceField(choices=Order.STATUSES, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Enter process status'}))
    info = forms.CharField(max_length=200,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control py-4', 'placeholder': 'Enter information'}))
    service_station = forms.ModelChoiceField(queryset=Station.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}),
                                             empty_label=None)

    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select'}),
        required=False,  # If you want orders to be optional
    )

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

        if owner:
            self.fields['workers'].queryset = Worker.objects.filter(
                Q(owner=owner)
            )
        elif manager:
            print(manager)
            self.fields['workers'].queryset = Worker.objects.filter(
                Q(owner=manager.owner.id)
            )
