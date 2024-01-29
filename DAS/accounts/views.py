from common.views import TitleMixin, BaseView, CreateAccountView, AccountProfileView
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import AccountProfileForm, CreateAccountUserForm, UserLoginForm, CreateManagerUserForm, CreateClientForm, \
    ClientForm
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

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, self.success_message)
    #     return redirect(self.success_url)


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
    form_class = AccountProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = get_object_or_404(AccountUsers, id=self.request.user.owner_id)
        clients = Client.objects.filter(owner=manager)
        context['clients'] = clients
        return context

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        managers = self.request.user.get_managers()
        if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class OwnerManagerAccountProfileView(AccountProfileView):
    template_name = "accounts/owner_manager_profile.html"
    title = 'DAS - manager account profile'
    profile = 'owner_manager_profile'


class OwnerAccountProfileView(AccountProfileView):
    template_name = 'accounts/owner_profile.html'
    title = 'DAS - owner account profile'
    profile = 'owner_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = get_object_or_404(AccountUsers, id=self.request.user.id)
        clients = Client.objects.filter(owner=owner)
        context['clients'] = [client for client in clients]
        return context

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        managers = self.request.user.get_managers()
        if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class AccountDelete(TitleMixin, DeleteView):
    model = AccountUsers
    success_url = reverse_lazy('accounts:reg')
    success_message = 'Account deleted successfully.'
    template_name = 'accounts/delete.html'
    title = 'DAS - account delete'

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Profile deleted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error, profile was not deleted.')
        return super().form_invalid(form)


class ClientOwnerCreateView(TitleMixin, CreateView):
    model = Client
    template_name = 'accounts/owner_create_client.html'
    form_class = CreateClientForm

    def form_valid(self, form):
        owner_id = get_object_or_404(AccountUsers, id=self.request.user.id)
        form.instance.owner = owner_id
        return super().form_valid(form)

    def get_success_url(self):
        # print(f"Debug: self.object.id = {self.object.id}")
        return reverse_lazy('accounts:owner_profile', args=(self.request.user.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class ClientManagerCreateView(TitleMixin, CreateView):
    model = Client
    template_name = 'accounts/manager_create_client.html'
    form_class = CreateClientForm

    def form_valid(self, form):
        form.instance.owner = self.request.user.owner
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:manager_profile', args=(self.request.user.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class ClientOwnerUpdateView(TitleMixin, UpdateView):
    model = Client
    template_name = 'accounts/owner_client.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy(f'accounts:client_owner', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Client, pk=kwargs['pk'])
        if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class ClientManagerUpdateView(TitleMixin, UpdateView):
    model = Client
    template_name = 'accounts/manager_client.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy(f'accounts:client_manager', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Client, pk=kwargs['pk'])
        # print(request.user.owner_id)
        # print(profile_user.owner_id)
        if ((request.user != profile_user or not request.user.is_active)
                and request.user.owner_id != profile_user.owner_id):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)
