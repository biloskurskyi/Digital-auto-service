from django import forms

from clients.models import Client


class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
