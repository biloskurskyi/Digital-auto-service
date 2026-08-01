from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class StyledForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control py-4')
            field.widget.attrs.setdefault('placeholder', field.label)


class RegistrationForm(StyledForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError(_('This email address is already used!'))
        return email


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
