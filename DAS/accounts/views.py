from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from common.views import (AccountDeleteView, AccountProfileView,
                          CreateAccountView, GeneratePDFView)

from .forms import CreateManagerUserForm
from .models import AccountUsers


class CreateManagerView(CreateAccountView):
    form_class = CreateManagerUserForm
    template_name = 'accounts/create_manager.html'
    success_message = ('Manager is create! For activation,'
                       ' he needs to confirm his/her identity in a letter at the post office')
    title = 'DAS - create manager'

    def get_success_url(self):
        creator_user = self.request.user
        return reverse_lazy('accounts:owner_profile', kwargs={'pk': creator_user.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if request.user != profile_user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class OwnerAccountProfileView(AccountProfileView):
    template_name = 'accounts/owner_profile.html'
    title = 'DAS - owner account profile'
    profile = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None


class ManagerAccountProfileView(AccountProfileView):
    template_name = "accounts/manager_profile.html"
    title = 'DAS - manager account profile'
    profile = 'manager_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is not None


class OwnerManagerAccountProfileView(AccountProfileView):
    template_name = "accounts/owner_manager_profile.html"
    title = 'DAS - manager account profile'
    profile = 'owner_manager_profile'

    def check_access(self, request, profile_user):
        if profile_user.id == request.user.id or (profile_user.id and profile_user.owner is None):
            raise Http404("User not found")
        return request.user.id == profile_user.owner.id and request.user.is_active


class OwnerAccountDelete(AccountDeleteView):
    template_name = 'accounts/delete_owner.html'

    def get_success_url(self):
        return reverse_lazy('accounts:reg')

    def check_access(self, request, profile_user):
        return request.user == profile_user


class ManagerAccountDelete(AccountDeleteView):
    template_name = 'accounts/delete_manager.html'
    reverse_page = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user.owner


class OwnerGeneratePDFView(GeneratePDFView):

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None


class ManagerGeneratePDFView(GeneratePDFView):
    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is not None
