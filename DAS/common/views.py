from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from accounts.forms import AccountProfileForm
from accounts.models import AccountUsers, Client


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class BaseView(TitleMixin, TemplateView):
    title = "DAS"


class CreateAccountView(TitleMixin, SuccessMessageMixin, CreateView):
    model = AccountUsers


class AccountProfileView(TitleMixin, UpdateView):
    model = AccountUsers
    form_class = AccountProfileForm
    profile = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        managers = self.object.get_managers()
        context['managers'] = managers

        # owner = get_object_or_404(AccountUsers, id=self.request.user.id)
        # clients = Client.objects.filter(owner=owner)
        # context['clients'] = [(client, client.id) for client in clients]

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     owner = get_object_or_404(AccountUsers, id=self.request.user.id)
    #     clients = Client.objects.filter(owner=owner)
    #     context['clients'] = [(client, client.id) for client in clients]
    #     # print([(client, client.id) for client in clients])
    #     return context

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.profile}', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        managers = self.request.user.get_managers()
        if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile.')
        return super().form_invalid(form)
