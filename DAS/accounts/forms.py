from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from accounts.models import AccountUsers


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = AccountUsers
        fields = ('username', 'password',)


class CreateAccountUserForm(UserCreationForm):
    class Meta:
        model = AccountUsers
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2',)
