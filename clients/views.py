from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from core.services import tenant_of
from core.views import FlashMessagesMixin

from .forms import ClientForm
from .models import Client


class ClientScopedMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Client.objects.for_tenant(tenant_of(self.request.user))


class ClientCreateView(FlashMessagesMixin, LoginRequiredMixin, CreateView):
    template_name = 'clients/client_new.html'
    form_class = ClientForm
    extra_context = {'title': 'DAS - Create client'}
    success_message = _('Client created successfully.')
    error_message = _('Error creating client.')

    def form_valid(self, form):
        form.instance.owner = tenant_of(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('client_edit', kwargs={'pk': self.object.pk})


class ClientUpdateView(FlashMessagesMixin, ClientScopedMixin, UpdateView):
    template_name = 'clients/client_edit.html'
    form_class = ClientForm
    extra_context = {'title': 'DAS - Client profile'}
    success_message = _('Client updated successfully.')
    error_message = _('Error updating client.')

    def get_context_data(self, **kwargs):
        return super().get_context_data(cars=self.object.car_set.all(), **kwargs)

    def get_success_url(self):
        return reverse('client_edit', kwargs={'pk': self.object.pk})


class ClientDeleteView(FlashMessagesMixin, ClientScopedMixin, DeleteView):
    template_name = 'clients/client_delete.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Client delete'}
    success_message = _('Client deleted successfully.')
