from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from accounts.models import AccountUsers


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = AccountUsers
        fields = ('username', 'password',)


class CreateAccountUserForm(UserCreationForm):
    class Meta:
        model = AccountUsers
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2',)
        db_table = 'account_users'


class AccountProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))

    class Meta:
        model = AccountUsers
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number',)

    def __init__(self, *args, **kwargs):
        super(AccountProfileForm, self).__init__(*args, **kwargs)

        # Приховуємо поле пароля
        self.fields['password'].widget = forms.HiddenInput()
