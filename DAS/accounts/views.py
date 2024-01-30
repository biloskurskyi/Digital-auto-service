from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from common.views import (AccountProfileView, BaseView, CreateAccountView,
                          TitleMixin, ClientCreateView, ClientUpdateView)

from .forms import (AccountProfileForm, ClientForm, CreateAccountUserForm,
                    CreateClientForm, CreateManagerUserForm, UserLoginForm)
from .models import AccountUsers, Client


class IndexView(BaseView):
    template_name = "accounts/base.html"
    title = "DAS"


class MianView(BaseView):
    template_name = "accounts/successful_login.html"
    title = "DAS - login success"


class UserLoginView(TitleMixin, LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    title = 'DAS - login'


class UserRegistrationView(CreateAccountView):
    form_class = CreateAccountUserForm
    template_name = 'accounts/registration.html'
    success_message = 'Registration is successfully done!'
    title = 'DAS - registration'
    success_url = reverse_lazy('accounts:log')


class CreateManagerView(CreateAccountView):
    form_class = CreateManagerUserForm
    template_name = 'accounts/create_manager.html'
    success_message = 'Manager is successfully create!'
    title = 'DAS - create manager'

    def get_success_url(self):
        creator_user = self.request.user
        return reverse_lazy('accounts:owner_profile', kwargs={'pk': creator_user.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ManagerAccountProfileView(AccountProfileView):
    template_name = "accounts/manager_profile.html"
    title = 'DAS - manager account profile'
    profile = 'manager_profile'

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user or not request.user.is_active or request.user.owner == None:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class OwnerAccountProfileView(AccountProfileView):
    template_name = 'accounts/owner_profile.html'
    title = 'DAS - owner account profile'
    profile = 'owner_profile'

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user or not request.user.is_active or request.user.owner != None:  # and profile_user.owner != request.user
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class OwnerManagerAccountProfileView(AccountProfileView):
    template_name = "accounts/owner_manager_profile.html"
    title = 'DAS - manager account profile'
    profile = 'owner_manager_profile'


class ClientOwnerCreateView(ClientCreateView):
    template_name = 'accounts/owner_create_client.html'
    path_name = 'owner_profile'

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user or not request.user.is_active or request.user.owner != None:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class ClientManagerCreateView(ClientCreateView):
    template_name = 'accounts/manager_create_client.html'
    path_name = 'manager_profile'

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user or not request.user.is_active or request.user.owner == None:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class ClientOwnerUpdateView(ClientUpdateView):
    template_name = 'accounts/owner_client.html'
    path_name = 'client_owner'


class ClientManagerUpdateView(ClientUpdateView):
    template_name = 'accounts/manager_client.html'
    path_name = 'client_manager'


class OwnerAccountDelete(TitleMixin, DeleteView):
    model = AccountUsers
    success_url = reverse_lazy('accounts:reg')
    template_name = 'accounts/delete_owner.html'
    title = 'DAS - account delete'

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Owner account deleted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error, account was not deleted.')
        return super().form_invalid(form)


class ManagerAccountDelete(TitleMixin, DeleteView):
    model = AccountUsers
    template_name = 'accounts/delete_manager.html'
    title = 'DAS - account delete'

    def get_success_url(self):
        return reverse_lazy('accounts:owner_profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(AccountUsers, pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().owner:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Manager account deleted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error, manager account was not deleted.')
        return super().form_invalid(form)


class OwnerClientAccountDelete(TitleMixin, DeleteView):
    model = Client
    template_name = 'accounts/delete_owner_client.html'
    title = 'DAS - account delete'

    def get_success_url(self):
        return reverse_lazy('accounts:owner_profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(Client, pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        print(request.user.id)
        print(self.get_object().owner.id)
        if request.user != self.get_object().owner:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Client account deleted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error, client account was not deleted.')
        return super().form_invalid(form)


class ManagerClientAccountDelete(TitleMixin, DeleteView):
    model = Client
    template_name = 'accounts/delete_owner_client.html'
    title = 'DAS - account delete'

    def get_success_url(self):
        return reverse_lazy('accounts:manager_profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(Client, pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Client, pk=kwargs['pk'])
        # print(profile_user.owner.id)
        # print(request.user.owner.id)
        if profile_user.owner != request.user.owner:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Client account deleted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error, client account was not deleted.')
        return super().form_invalid(form)
