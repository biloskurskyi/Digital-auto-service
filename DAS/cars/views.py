from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.models import AccountUsers
from cars.forms import CreateCarForm
from cars.models import Car
from clients.models import Client
from common.views import TitleMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class CarManagerCreateView(TitleMixin, CreateView):
    model = Car
    form_class = CreateCarForm
    title = 'create car'
    template_name = 'cars/manager_create_car.html'
    path_name = 'manager_owner'

    def get_success_url(self):
        return reverse_lazy(f'accounts:manager_profile', args=(self.request.user.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['manager'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if not (request.user == profile_user and request.user.is_active and request.user.owner is not None):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class CarOwnerCreateView(TitleMixin, CreateView):
    model = Car
    form_class = CreateCarForm
    title = 'create car'
    template_name = 'cars/owner_create_car.html'
    path_name = 'client_owner'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user  # Pass the owner to the form
        return kwargs

    def get_success_url(self):
        return reverse_lazy(f'accounts:owner_profile', args=(self.request.user.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if not (request.user == profile_user and request.user.is_active and request.user.owner is None):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class CarOwnerUpdateView(TitleMixin, UpdateView):
    template_name = 'cars/owner_car.html'
    path_name = 'car_owner'
    model = Car
    form_class = CreateCarForm
    title = 'car update'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('cars:car_owner', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Car, pk=kwargs['pk'])
        if self.path_name == 'car_manager':
            if ((request.user != profile_user or not request.user.is_active)
                    and request.user.owner_id != profile_user.client.owner_id):
                raise Http404("User not found")
        elif self.path_name == 'car_owner':
            if ((request.user != profile_user or not request.user.is_active)
                    and profile_user.client.owner != request.user):
                raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class CarManagerUpdateView(TitleMixin, UpdateView):
    template_name = 'cars/manager_car.html'
    path_name = 'car_manager'
    model = Car
    form_class = CreateCarForm
    title = 'car update'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['manager'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('cars:car_manager', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Car, pk=kwargs['pk'])
        if self.path_name == 'car_manager':
            if ((request.user != profile_user or not request.user.is_active)
                    and request.user.owner_id != profile_user.client.owner_id):
                raise Http404("User not found")
        elif self.path_name == 'car_owner':
            if ((request.user != profile_user or not request.user.is_active)
                    and profile_user.client.owner != request.user):
                raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class OwnerCarAccountDelete(TitleMixin, DeleteView):
    model = Car
    template_name = 'cars/owner_delete_car.html'
    title = 'DAS - car delete'
    reverse_page = 'owner_profile'

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', kwargs={'pk': self.request.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(self.model, pk=kwargs['pk'])

        if not request.user == profile_user.client.owner:
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)


class ManagerCarAccountDelete(TitleMixin, DeleteView):
    model = Car
    template_name = 'cars/manager_delete_car.html'
    title = 'DAS - car delete'
    reverse_page = 'manager_profile'

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', kwargs={'pk': self.request.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(self.model, pk=kwargs['pk'])

        if not profile_user.client.owner == request.user.owner:
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)
