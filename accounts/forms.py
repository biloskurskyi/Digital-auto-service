from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from core.forms import StyledForm

from .models import User


class UniqueActiveEmailMixin:
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError(_('This email address is already used!'))
        return email


class RegistrationForm(UniqueActiveEmailMixin, StyledForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')


class ManagerInviteForm(UniqueActiveEmailMixin, StyledForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')


class ProfileForm(StyledForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('username', 'email', 'is_active'):
            self.fields[name].disabled = True


class LoginForm(StyledForm, AuthenticationForm):
    def clean(self):
        try:
            return super().clean()
        except forms.ValidationError:
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = User.objects.filter(username=username, is_active=False).first()
            if user and password and user.check_password(password):
                raise forms.ValidationError(_('Please verify your email before logging in.'), code='unverified')
            raise


class PasswordResetEmailForm(StyledForm, PasswordResetForm):
    pass


class PasswordSetForm(StyledForm, SetPasswordForm):
    pass
