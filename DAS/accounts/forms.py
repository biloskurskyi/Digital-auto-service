import secrets
import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CheckboxInput
from django.utils.timezone import now

from accounts.models import AccountUsers, EmailVerification


class CreateManagerUserForm(UserCreationForm):
    # email = forms.EmailField()
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter last name'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter username'}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter email'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter phone number'}))

    class Meta:
        model = AccountUsers
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateManagerUserForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        user = super(CreateManagerUserForm, self).save(commit=False)
        if commit:
            password = secrets.token_urlsafe(8)
            user.set_password(password)
            user.owner_id = self.request.user.id if self.request.user.is_authenticated else None
            user.save()

            expiration = now() + timedelta(hours=24)
            record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
            record.send_verification_email(password)
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        users_with_email = AccountUsers.objects.filter(email=email)
        if users_with_email.exists():
            user = users_with_email.first()
            if user.is_active:
                raise forms.ValidationError("This email address is already used!")
        return email


class AccountProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    # is_active = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': 'readonly'}))
    is_active = forms.BooleanField(required=False, widget=CheckboxInput(attrs={'disabled': 'true'}))

    class Meta:
        model = AccountUsers
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AccountProfileForm, self).__init__(*args, **kwargs)
        # is_active_value = self.initial.get('is_active', False)
        # self.fields['is_active'].initial = "Yes" if self.initial.get('is_active') else "No"

        self.fields['password'].widget = forms.HiddenInput()

    # def clean_is_active(self):
    #     is_active = self.cleaned_data['is_active']
    #     return "Yes" if is_active else "No"
