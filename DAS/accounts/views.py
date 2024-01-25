from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from .forms import AccountProfileForm, CreateAccountUserForm, UserLoginForm
from .models import AccountUsers


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class IndexView(TitleMixin, TemplateView):
    template_name = "accounts/base.html"
    title = "DAS"


class MianView(TitleMixin, TemplateView):
    template_name = "accounts/successful_login.html"
    title = "DAS - login success"


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = AccountUsers
    form_class = CreateAccountUserForm
    template_name = 'accounts/registration.html'
    success_message = 'Registration is successfully done!'
    title = 'DAS - registration'
    success_url = reverse_lazy('accounts:log')

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, self.success_message)
    #     return redirect(self.success_url)


class UserLoginView(TitleMixin, LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    title = 'DAS - login'


class AccountProfile(TitleMixin, UpdateView):
    model = AccountUsers
    form_class = AccountProfileForm
    template_name = "accounts/profile.html"
    title = 'DAS - account profile'

    def get_success_url(self):
        return reverse_lazy('accounts:ok', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user:
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
