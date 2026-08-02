from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, FormView, TemplateView, UpdateView

from core.views import FlashMessagesMixin, OwnerRequiredMixin

from . import services
from .forms import LoginForm, ManagerInviteForm, PasswordResetEmailForm, PasswordSetForm, ProfileForm, RegistrationForm
from .models import User


class LandingView(TemplateView):
    template_name = 'accounts/landing.html'
    extra_context = {'title': 'DAS'}


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('verify_sent')
    extra_context = {'title': 'DAS - Registration'}

    def form_valid(self, form):
        services.register_owner(self.request, form)
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    extra_context = {'title': 'DAS - Login'}


class LoginSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/login_success.html'
    extra_context = {'title': 'DAS - Login success'}


class VerifyView(TemplateView):
    template_name = 'accounts/verify_success.html'
    extra_context = {'title': 'DAS - Email verification'}

    def get(self, request, *args, **kwargs):
        verification = services.pending_verification(kwargs['pk'], kwargs['email'], kwargs['code'])
        if verification is None:
            return redirect('verify_invalid')
        if not verification.user.has_usable_password():
            return self.render_set_password(PasswordSetForm(verification.user))
        services.complete_verification(verification)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        verification = services.pending_verification(kwargs['pk'], kwargs['email'], kwargs['code'])
        if verification is None:
            return redirect('verify_invalid')
        form = PasswordSetForm(verification.user, request.POST)
        if not form.is_valid():
            return self.render_set_password(form)
        services.activate_manager(verification, form)
        return super().get(request, *args, **kwargs)

    def render_set_password(self, form):
        context = {'form': form, 'title': 'DAS - Set your password'}
        return render(self.request, 'accounts/manager_set_password.html', context)


class VerifySentView(TemplateView):
    template_name = 'accounts/verify_sent.html'
    extra_context = {'title': 'DAS - Confirm email'}


class VerifyInvalidView(TemplateView):
    template_name = 'accounts/verify_invalid.html'
    extra_context = {'title': 'DAS - Email not verified'}


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = PasswordResetEmailForm
    extra_context = {'title': 'DAS - Password reset'}


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    extra_context = {'title': 'DAS - Password reset sent'}


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = PasswordSetForm
    extra_context = {'title': 'DAS - Set new password'}


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    extra_context = {'title': 'DAS - Password reset complete'}


class DashboardView(FlashMessagesMixin, LoginRequiredMixin, UpdateView):
    template_name = 'accounts/dashboard.html'
    form_class = ProfileForm
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Dashboard'}
    success_message = _('Profile updated successfully.')
    error_message = _('Error updating profile.')

    def get_object(self, queryset=None):
        return self.request.user


class AccountDeleteView(OwnerRequiredMixin, DeleteView):
    template_name = 'accounts/account_delete.html'
    success_url = reverse_lazy('register')
    extra_context = {'title': 'DAS - Account delete'}

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        services.delete_owner_account(self.object)
        messages.success(self.request, _('Account deleted successfully.'))
        return HttpResponseRedirect(self.get_success_url())


class ManagerCreateView(FlashMessagesMixin, OwnerRequiredMixin, FormView):
    template_name = 'accounts/manager_new.html'
    form_class = ManagerInviteForm
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Create manager'}
    success_message = _('Manager created. An activation link has been emailed to them.')

    def form_valid(self, form):
        services.invite_manager(self.request, form, self.request.user)
        return super().form_valid(form)


class ManagerUpdateView(FlashMessagesMixin, LoginRequiredMixin, UpdateView):
    template_name = 'accounts/manager_edit.html'
    form_class = ProfileForm
    extra_context = {'title': 'DAS - Manager profile'}
    success_message = _('Profile updated successfully.')
    error_message = _('Error updating profile.')

    def get_queryset(self):
        return User.objects.for_tenant(self.request.user)

    def get_success_url(self):
        return reverse('manager_edit', kwargs={'pk': self.object.pk})


class ManagerDeleteView(FlashMessagesMixin, LoginRequiredMixin, DeleteView):
    template_name = 'accounts/manager_delete.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Account delete'}
    success_message = _('Account deleted successfully.')

    def get_queryset(self):
        return User.objects.for_tenant(self.request.user)
