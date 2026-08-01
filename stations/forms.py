from django import forms

from core.forms import StyledForm

from .models import Station


class StationForm(StyledForm, forms.ModelForm):
    class Meta:
        model = Station
        fields = ('name', 'address')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.instance.owner = user
        elif self.instance.owner != user:
            for field in self.fields.values():
                field.disabled = True

    def _get_validation_exclusions(self):
        return super()._get_validation_exclusions() - {'owner'}
