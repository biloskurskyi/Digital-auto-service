from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from . import services
from .forms import LoginForm, PasswordResetEmailForm, PasswordSetForm, RegistrationForm


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
        if not services.verify_email(kwargs['pk'], kwargs['email'], kwargs['code']):
            return redirect('verify_invalid')
        return super().get(request, *args, **kwargs)


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
