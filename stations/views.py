from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from core.views import FlashMessagesMixin, OwnerRequiredMixin, TenantScopedMixin

from .forms import StationForm
from .models import Station


class StationFormMixin:
    form_class = StationForm

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'user': self.request.user}

    def get_success_url(self):
        return reverse('station_edit', kwargs={'pk': self.object.pk})


class StationCreateView(FlashMessagesMixin, StationFormMixin, OwnerRequiredMixin, CreateView):
    template_name = 'stations/station_new.html'
    extra_context = {'title': 'DAS - Create station'}
    success_message = _('Station created successfully.')
    error_message = _('Error creating station.')


class StationUpdateView(FlashMessagesMixin, StationFormMixin, TenantScopedMixin, UpdateView):
    model = Station
    template_name = 'stations/station_edit.html'
    extra_context = {'title': 'DAS - Station profile'}
    success_message = _('Station updated successfully.')
    error_message = _('Error updating station.')


class StationDeleteView(FlashMessagesMixin, OwnerRequiredMixin, TenantScopedMixin, DeleteView):
    model = Station
    template_name = 'stations/station_delete.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Station delete'}
    success_message = _('Station deleted successfully.')
