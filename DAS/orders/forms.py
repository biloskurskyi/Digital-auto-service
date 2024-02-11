from django import forms

from cars.models import Car

from .models import Order


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

        super(CreateOrderForm, self).__init__(*args, **kwargs)

        if owner:
            self.fields['client'].queryset = owner.client_set.all()
        if manager:
            owner = manager.owner if manager.owner else manager
            self.fields['client'].queryset = owner.client_set.all()

        self.fields['car'].queryset = Car.objects.none()

        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                self.fields['car'].queryset = Car.objects.filter(client_id=client_id)
            except (ValueError, TypeError):
                pass
        elif self.instance and hasattr(self.instance, 'client') and self.instance.client:
            self.fields['car'].queryset = self.instance.client.car_set.all()


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

        super(UpdateOrderForm, self).__init__(*args, **kwargs)

        if owner:
            self.fields['client'].queryset = owner.client_set.all()
        if manager:
            owner = manager.owner if manager.owner else manager
            self.fields['client'].queryset = owner.client_set.all()

        self.fields['client'].disabled = True
        self.fields['car'].disabled = True
