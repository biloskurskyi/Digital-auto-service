from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from core.services import tenant_of


class FlashMessagesMixin:
    success_message = ''
    error_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class OwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.owner_id is not None:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class TenantScopedMixin(LoginRequiredMixin):
    def get_queryset(self):
        return self.model.objects.for_tenant(tenant_of(self.request.user))
