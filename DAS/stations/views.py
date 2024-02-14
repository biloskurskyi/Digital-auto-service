# from common.views import ClientCreateView, ClientDeleteView, ClientUpdateView
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from accounts.models import AccountUsers
from clients.forms import CreateClientForm
from clients.models import Client
from common.views import TitleMixin, StationCreateView, StationUpdateView
from stations.forms import CreateStationForm
from stations.models import Station


class StationOwnerCreateView(StationCreateView):
    path_name = 'owner_profile'
    template_name = 'stations/owner_create_station.html'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None


#


class StationOwnerUpdateView(StationUpdateView):
    template_name = 'stations/owner_station.html'
    path_name = 'station_owner'


class StationManagerUpdateView(StationUpdateView):
    template_name = 'stations/manager_station.html'
    path_name = 'station_manager'


class StationDeleteView(TitleMixin, DeleteView):
    model = Station
    title = 'DAS - station delete'
    form_valid_info = 'Station deleted successfully.'
    form_invalid_info = 'Error, station was not deleted.'
    reverse_page = 'owner_profile'
    template_name = 'stations/owner_delete_station.html'

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', kwargs={'pk': self.request.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(self.model, pk=kwargs['pk'])

        if not (request.user == profile_user.owner):
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)

#
#
# class ClientManagerUpdateView(ClientUpdateView):
#     template_name = 'clients/manager_client.html'
#     path_name = 'client_manager'
#
#
# class OwnerClientAccountDelete(ClientDeleteView):
#     template_name = 'clients/delete_owner_client.html'
#     reverse_page = 'owner_profile'
#
#     def check_access(self, request, profile_user):
#         return request.user == profile_user.owner
#
#
# class ManagerClientAccountDelete(ClientDeleteView):
#     template_name = 'clients/delete_manager_client.html'
#     reverse_page = 'manager_profile'
#
#     def check_access(self, request, profile_user):
#         return profile_user.owner == request.user.owner
