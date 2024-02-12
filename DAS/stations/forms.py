from django import forms

# from location_field.models.plain import PlainLocationField

from .models import Station


class CreateStationForm(forms.ModelForm):
    # address = PlainLocationField(based_fields=['address'], zoom=7)

    class Meta:
        model = Station
        fields = '__all__'
        exclude = ('owner',)

    # def __init__(self, *args, **kwargs):
    #     super(CreateStationForm, self).__init__(*args, **kwargs)
    #     self.request = kwargs.pop('request', None)
    #     self.fields['service_station'].queryset = Station.get_owned_stations(self.request.user)
