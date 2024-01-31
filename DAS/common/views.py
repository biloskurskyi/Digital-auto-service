from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, TemplateView,
                                  UpdateView)

from accounts.forms import AccountProfileForm, CreateAccountUserForm
from accounts.models import AccountUsers
from clients.forms import ClientForm, CreateClientForm
from clients.models import Client


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class BaseView(TitleMixin, TemplateView):
    title = "DAS"


class CreateAccountView(TitleMixin, SuccessMessageMixin, CreateView):
    model = AccountUsers


class AccountProfileView(TitleMixin, UpdateView):
    model = AccountUsers
    form_class = AccountProfileForm
    profile = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        managers = self.object.get_managers()
        context['managers'] = managers

        if self.request.user.owner is not None:
            manager = get_object_or_404(AccountUsers, id=self.request.user.owner_id)
            clients = Client.objects.filter(owner=manager)
            context['clients'] = clients
        else:
            owner = get_object_or_404(AccountUsers, id=self.request.user.id)
            clients = Client.objects.filter(owner=owner)
            context['clients'] = [client for client in clients]
        return context

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.profile}', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile.')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class ClientCreateView(TitleMixin, CreateView):
    model = Client
    form_class = CreateClientForm
    path_name = 'profile'
    title = 'create client'

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.path_name}', args=(self.request.user.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.path_name == 'manager_profile':
            form.instance.owner = self.request.user.owner
            messages.success(self.request, 'Client created successfully.')
        elif self.path_name == 'owner_profile':
            owner_id = get_object_or_404(AccountUsers, id=self.request.user.id)
            form.instance.owner = owner_id
            messages.success(self.request, 'Client created successfully.')
        return super().form_valid(form)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class ClientUpdateView(TitleMixin, UpdateView):
    model = Client
    form_class = ClientForm
    path_name = 'profile'
    title = 'client update'

    def get_success_url(self):
        messages.success(self.request, 'Client profile updated successfully.')
        return reverse_lazy(f'clients:{self.path_name}', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Client, pk=kwargs['pk'])
        if self.path_name == 'client_manager':
            if ((request.user != profile_user or not request.user.is_active)
                    and request.user.owner_id != profile_user.owner_id):
                raise Http404("User not found")
        elif self.path_name == 'client_owner':
            if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
                raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class DeleteAccountView(TitleMixin, DeleteView):
    form_valid_info = 'Account deleted successfully.'
    form_invalid_info = 'Account was not deleted.'
    reverse_page = ''
    model = ''

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', kwargs={'pk': self.request.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(self.model, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")
