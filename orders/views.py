from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import BaseDetailView

from clients.models import Client
from core.services import tenant_of
from core.views import FlashMessagesMixin, TenantScopedMixin

from .forms import OrderForm
from .models import Order
from .services import save_order


class OrderFormMixin:
    form_class = OrderForm

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'tenant': tenant_of(self.request.user)}

    def get_success_url(self):
        return reverse('order_edit', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = save_order(form)
        return HttpResponseRedirect(self.get_success_url())


class OrderCreateView(FlashMessagesMixin, OrderFormMixin, LoginRequiredMixin, CreateView):
    template_name = 'orders/order_new.html'
    extra_context = {'title': 'DAS - Create order'}
    success_message = _('Order created successfully.')
    error_message = _('Error creating order.')


class OrderUpdateView(FlashMessagesMixin, OrderFormMixin, TenantScopedMixin, UpdateView):
    model = Order
    template_name = 'orders/order_edit.html'
    extra_context = {'title': 'DAS - Order profile'}
    success_message = _('Order updated successfully.')
    error_message = _('Error updating order.')


class OrderDeleteView(FlashMessagesMixin, TenantScopedMixin, DeleteView):
    model = Order
    template_name = 'orders/order_delete.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Order delete'}
    success_message = _('Order deleted successfully.')


class ClientCarsView(TenantScopedMixin, BaseDetailView):
    model = Client

    def render_to_response(self, context):
        return JsonResponse({'car_choices': [[car.pk, str(car)] for car in self.object.car_set.all()]})
