from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, FormView, TemplateView, UpdateView

from . import services
from .forms import LoginForm, ManagerInviteForm, PasswordResetEmailForm, PasswordSetForm, ProfileForm, RegistrationForm
from .models import User


class OwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.owner_id is not None:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ProfileMessagesMixin:
    def form_valid(self, form):
        messages.success(self.request, _('Profile updated successfully.'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Error updating profile.'))
        return super().form_invalid(form)


class DeletedMessageMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Account deleted successfully.'))
        return response


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


class DashboardView(ProfileMessagesMixin, LoginRequiredMixin, UpdateView):
    template_name = 'accounts/dashboard.html'
    form_class = ProfileForm
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Dashboard'}

    def get_object(self, queryset=None):
        return self.request.user


class AccountDeleteView(DeletedMessageMixin, OwnerRequiredMixin, DeleteView):
    template_name = 'accounts/account_delete.html'
    success_url = reverse_lazy('register')
    extra_context = {'title': 'DAS - Account delete'}

    def get_object(self, queryset=None):
        return self.request.user


class ManagerCreateView(OwnerRequiredMixin, FormView):
    template_name = 'accounts/manager_new.html'
    form_class = ManagerInviteForm
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Create manager'}

    def form_valid(self, form):
        services.invite_manager(self.request, form, self.request.user)
        messages.success(self.request, _('Manager created. An activation link has been emailed to them.'))
        return super().form_valid(form)


class ManagerUpdateView(ProfileMessagesMixin, LoginRequiredMixin, UpdateView):
    template_name = 'accounts/manager_edit.html'
    form_class = ProfileForm
    extra_context = {'title': 'DAS - Manager profile'}

    def get_queryset(self):
        return User.objects.for_tenant(self.request.user)

    def get_success_url(self):
        return reverse('manager_edit', kwargs={'pk': self.object.pk})


class ManagerDeleteView(DeletedMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'accounts/manager_delete.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'title': 'DAS - Account delete'}

    def get_queryset(self):
        return User.objects.for_tenant(self.request.user)
