from common.views import TitleMixin, BaseView, CreateAccountView
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import AccountProfileForm, CreateAccountUserForm, UserLoginForm, CreateManagerUserForm
from .models import AccountUsers


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


class ManagerAccountProfileView(TitleMixin, UpdateView):
    model = AccountUsers
    form_class = AccountProfileForm
    template_name = "accounts/manager_profile.html"
    title = 'DAS - manager account profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        managers = self.object.get_managers()
        context['managers'] = managers
        return context

    def get_success_url(self):
        return reverse_lazy('accounts:profile', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        managers = self.request.user.get_managers()
        if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile.')
        return super().form_invalid(form)


class OwnerManagerAccountProfileView(TitleMixin, UpdateView):
    model = AccountUsers
    form_class = AccountProfileForm
    template_name = "accounts/owner_manager_profile.html"
    title = 'DAS - manager account profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        managers = self.object.get_managers()
        context['managers'] = managers
        return context

    def get_success_url(self):
        return reverse_lazy('accounts:profile', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        managers = self.request.user.get_managers()
        if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile.')
        return super().form_invalid(form)


class OwnerAccountProfileView(TitleMixin, UpdateView):
    model = AccountUsers
    form_class = AccountProfileForm
    template_name = "accounts/owner_profile.html"
    title = 'DAS - owner account profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        managers = self.object.get_managers()
        context['managers'] = managers
        return context

    def get_success_url(self):
        return reverse_lazy('accounts:owner_profile', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        managers = self.request.user.get_managers()
        if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile.')
        return super().form_invalid(form)


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
