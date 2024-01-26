import random
import secrets
import string

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.mail import send_mail

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


class CreateManagerUserForm(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = AccountUsers
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateManagerUserForm, self).__init__(*args, **kwargs)

        password = secrets.token_urlsafe(12)

        self.fields['password1'].initial = password
        self.fields['password2'].initial = password

        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()

        # self.fields['password1'].widget = forms.TextInput(
        #     attrs={'readonly': 'readonly', 'style': 'background-color: #ddd;'})
        # self.fields['password2'].widget = forms.TextInput(
        #     attrs={'readonly': 'readonly', 'style': 'background-color: #ddd;'})

    def save(self, commit=True):
        user = super(CreateManagerUserForm, self).save(commit=False)
        user.owner_id = self.request.user.id if self.request.user.is_authenticated else None

        if commit:
            user.save()

            # subject = 'Your Account Information'
            # message = f'Your username: {user.username}\nYour password: {user.password}'
            # from_email = 'your_email@example.com'
            # recipient_list = [user.email]
            #
            # send_mail(subject, message, from_email, recipient_list)

        return user


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

        self.fields['password'].widget = forms.HiddenInput()
