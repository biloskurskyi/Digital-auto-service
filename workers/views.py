from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from core.services import tenant_of
from core.views import FlashMessagesMixin, TenantScopedMixin

from .forms import WorkerForm
from .models import Worker


class WorkerFormMixin:
    form_class = WorkerForm

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'tenant': tenant_of(self.request.user)}

    def get_success_url(self):
        return reverse('worker_edit', kwargs={'pk': self.object.pk})


class WorkerCreateView(FlashMessagesMixin, WorkerFormMixin, LoginRequiredMixin, CreateView):
    template_name = 'workers/worker_new.html'
    extra_context = {'title': 'DAS - Create worker'}
    success_message = _('Worker created successfully.')
    error_message = _('Error creating worker.')

    def form_valid(self, form):
        form.instance.owner = tenant_of(self.request.user)
        return super().form_valid(form)


class WorkerUpdateView(FlashMessagesMixin, WorkerFormMixin, TenantScopedMixin, UpdateView):
    model = Worker
    template_name = 'workers/worker_edit.html'
    extra_context = {'title': 'DAS - Worker profile'}
    success_message = _('Worker updated successfully.')
    error_message = _('Error updating worker.')


class WorkerDeleteView(FlashMessagesMixin, TenantScopedMixin, DeleteView):
    model = Worker
    template_name = 'workers/worker_delete.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Worker delete'}
    success_message = _('Worker deleted successfully.')
