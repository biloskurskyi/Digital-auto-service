from django import forms

from core.forms import StyledForm
from orders.models import Order

from .models import Worker


class WorkerForm(StyledForm, forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('first_name', 'last_name', 'date_of_birth', 'years_of_experience', 'skills', 'salary', 'orders')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'orders': forms.CheckboxSelectMultiple,
        }

    def __init__(self, tenant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['orders'].queryset = Order.objects.for_tenant(tenant).select_related('client', 'car')
