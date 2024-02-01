from django import forms

from .models import Car


class CreateCarForm(forms.ModelForm):
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
