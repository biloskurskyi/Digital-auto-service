from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from core.services import tenant_of
from core.views import FlashMessagesMixin

from .forms import CarForm
from .models import Car


class CarScopedMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Car.objects.for_tenant(tenant_of(self.request.user))


class CarFormMixin:
    form_class = CarForm

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'tenant': tenant_of(self.request.user)}

    def get_success_url(self):
        return reverse('car_edit', kwargs={'pk': self.object.pk})


class CarCreateView(FlashMessagesMixin, CarFormMixin, LoginRequiredMixin, CreateView):
    template_name = 'cars/car_new.html'
    extra_context = {'title': 'DAS - Create car'}
    success_message = _('Car created successfully.')
    error_message = _('Error creating car.')


class CarUpdateView(FlashMessagesMixin, CarFormMixin, CarScopedMixin, UpdateView):
    template_name = 'cars/car_edit.html'
    extra_context = {'title': 'DAS - Car profile'}
    success_message = _('Car updated successfully.')
    error_message = _('Error updating car.')


class CarDeleteView(FlashMessagesMixin, CarScopedMixin, DeleteView):
    template_name = 'cars/car_delete.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Car delete'}
    success_message = _('Car deleted successfully.')
