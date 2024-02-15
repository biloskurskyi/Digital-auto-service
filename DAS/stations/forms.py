from django import forms

from .models import Station

# from location_field.models.plain import PlainLocationField



class CreateStationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter station name'}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter address'}))

    class Meta:
        model = Station
        fields = '__all__'
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        username = kwargs.pop('username', None)
        super(CreateStationForm, self).__init__(*args, **kwargs)
        if owner:
            self.owner = owner
        else:
            self.owner = None
        # print(owner, username)
        # print(owner == username)
        if owner != username:
            print('ok')
            self.fields['name'].disabled = True
            self.fields['address'].disabled = True

# def __init__(self, *args, **kwargs):
#     super(CreateStationForm, self).__init__(*args, **kwargs)
#     self.request = kwargs.pop('request', None)
#     self.fields['service_station'].queryset = Station.get_owned_stations(self.request.user)
