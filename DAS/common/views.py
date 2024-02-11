from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, TemplateView,
                                  UpdateView)
from xhtml2pdf import pisa

from accounts.forms import AccountProfileForm
from accounts.models import AccountUsers
from cars.forms import CreateCarForm
from cars.models import Car
from clients.forms import ClientForm, CreateClientForm
from clients.models import Client
from orders.forms import CreateOrderForm, UpdateOrderForm
from orders.models import Order
from stations.forms import CreateStationForm
from stations.models import Station


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

        if self.request.user.owner is not None:
            manager = get_object_or_404(AccountUsers, id=self.request.user.owner_id)
            clients = Client.objects.filter(owner=manager)
            context['clients'] = clients
            cars = Car.objects.filter(client__owner=manager)
            context['cars'] = cars
            orders = Order.objects.filter(client__owner=manager)
            context['orders'] = orders
            stations = Station.objects.filter(owner=manager)
            context['stations'] = stations
        else:
            owner = get_object_or_404(AccountUsers, id=self.request.user.id)
            clients = Client.objects.filter(owner=owner)
            context['clients'] = [client for client in clients]
            cars = Car.objects.filter(client__owner=owner)
            context['cars'] = cars
            orders = Order.objects.filter(client__owner=owner)
            context['orders'] = orders
            stations = Station.objects.filter(owner=owner)
            context['stations'] = stations
        return context

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.profile}', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile.')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class AccountDeleteView(TitleMixin, DeleteView):
    form_valid_info = 'Account deleted successfully.'
    form_invalid_info = 'Account was not deleted.'
    reverse_page = ''
    model = AccountUsers
    title = 'DAS - account delete'

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

        if not self.check_access(request, profile_user):
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class ClientCreateView(TitleMixin, CreateView):
    model = Client
    form_class = CreateClientForm
    path_name = 'profile'
    title = 'create client'

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.path_name}', args=(self.request.user.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.path_name == 'manager_profile':
            form.instance.owner = self.request.user.owner
            messages.success(self.request, 'Client created successfully.')
        elif self.path_name == 'owner_profile':
            owner_id = get_object_or_404(AccountUsers, id=self.request.user.id)
            form.instance.owner = owner_id
            messages.success(self.request, 'Client created successfully.')
        return super().form_valid(form)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class ClientUpdateView(TitleMixin, UpdateView):
    model = Client
    form_class = ClientForm
    path_name = 'profile'
    title = 'client update'

    def get_success_url(self):
        messages.success(self.request, 'Client profile updated successfully.')
        return reverse_lazy(f'clients:{self.path_name}', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Client, pk=kwargs['pk'])
        if self.path_name == 'client_manager':
            if ((request.user != profile_user or not request.user.is_active)
                    and request.user.owner_id != profile_user.owner_id):
                raise Http404("User not found")
        elif self.path_name == 'client_owner':
            if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
                raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class ClientDeleteView(TitleMixin, DeleteView):
    model = Client
    title = 'DAS - client delete'
    form_valid_info = 'Client account deleted successfully.'
    form_invalid_info = 'Error, client account was not deleted.'
    reverse_page = ''

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

        if not self.check_access(request, profile_user):
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class CarCreateView(TitleMixin, CreateView):
    form_valid_info = 'Car was created successfully.'
    form_invalid_info = 'Car was not created.'
    model = Car
    form_class = CreateCarForm
    title = 'create car'
    reverse_page = ''
    creator_type = ''

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', args=(self.request.user.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs[self.creator_type] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if not self.check_access(request, profile_user):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class CarUpdateView(TitleMixin, UpdateView):
    form_valid_info = 'Car was update successfully.'
    form_invalid_info = 'Car was not updated.'
    model = Car
    form_class = CreateCarForm
    title = 'car update'
    reverse_page = ''
    creator_type = ''
    path_name = ''

    def get_success_url(self):
        return reverse_lazy(f'cars:{self.reverse_page}', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs[self.creator_type] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)

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


class CarDeleteView(TitleMixin, DeleteView):
    model = Car
    title = 'DAS - car delete'
    reverse_page = ''
    form_valid_info = 'Car deleted successfully.'
    form_invalid_info = 'Car was not deleted.'

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', kwargs={'pk': self.request.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(self.model, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)


class GeneratePDFView(TitleMixin, View):
    title = "pdf data"
    template_name = 'accounts/pdf_clients.html'

    def get_context_data(self, **kwargs):
        context = {}

        if self.request.user.owner is not None:
            manager = get_object_or_404(AccountUsers, id=self.request.user.owner_id)
            managers = None
            clients = Client.objects.filter(owner=manager)
            cars = Car.objects.filter(client__owner=manager)
            orders = Order.objects.filter(car__order__client__owner=manager)
        else:
            owner = get_object_or_404(AccountUsers, id=self.request.user.id)
            managers = AccountUsers.objects.filter(owner__isnull=False, owner=owner).distinct()
            clients = Client.objects.filter(owner=owner)
            cars = Car.objects.filter(client__owner=owner)
            orders = Order.objects.filter(car__order__client__owner=owner)
        context['managers'] = managers
        context['clients'] = clients
        context['cars'] = cars
        context['orders'] = orders
        context['username'] = self.request.user.username
        return context

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if not self.check_access(request, profile_user):  # not
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(pk=kwargs['pk'])

        template = get_template(self.template_name)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="clients_report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class OrderCreateView(TitleMixin, CreateView):
    form_valid_info = 'Order was created successfully.'
    form_invalid_info = 'Order was not created.'
    model = Order
    form_class = CreateOrderForm
    title = 'Create order'

    reverse_page = ''
    creator_type = ''

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', args=(self.request.user.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs[self.creator_type] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])
        if not self.check_access(request, profile_user):  # not
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class OrderUpdateView(TitleMixin, UpdateView):
    creator_type = ''
    reverse_page = path_name = ''

    form_valid_info = 'Order was update successfully.'
    form_invalid_info = 'Order was not updated.'
    model = Order
    form_class = UpdateOrderForm
    title = 'Order update'

    def get_success_url(self):
        return reverse_lazy(f'orders:{self.reverse_page}', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs[self.creator_type] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Order, pk=kwargs['pk'])
        if self.path_name == 'order_manager':
            if ((request.user != profile_user or not request.user.is_active)
                    and request.user.owner_id != profile_user.client.owner_id):
                raise Http404("User not found")
        elif self.path_name == 'order_owner':
            if ((request.user != profile_user or not request.user.is_active)
                    and profile_user.client.owner != request.user):
                raise Http404("User not found")
        else:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class OrderDeleteView(TitleMixin, DeleteView):
    model = Order
    title = 'DAS - article delete'
    form_valid_info = 'Order deleted successfully.'
    form_invalid_info = 'Order was not deleted.'
    reverse_page = ''

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.reverse_page}', kwargs={'pk': self.request.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(self.model, pk=kwargs['pk'])
        print(request.user)
        if not self.check_access(request, profile_user):
            raise Http404("User not found")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'{self.form_valid_info}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'{self.form_invalid_info}')
        return super().form_invalid(form)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class StationCreateView(TitleMixin, CreateView):
    model = Station
    form_class = CreateStationForm
    path_name = 'profile'
    title = 'create station'

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.path_name}', args=(self.request.user.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.path_name == 'manager_profile':
            form.instance.owner = self.request.user.owner
            messages.success(self.request, 'Client created successfully.')
        elif self.path_name == 'owner_profile':
            owner_id = get_object_or_404(AccountUsers, id=self.request.user.id)
            form.instance.owner = owner_id
            messages.success(self.request, 'Client created successfully.')
        return super().form_valid(form)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class StationUpdateView(TitleMixin, UpdateView):
    path_name = 'station'
    model = Station
    form_class = CreateStationForm
    title = 'station update'

    def get_success_url(self):
        messages.success(self.request, 'Station profile updated successfully.')
        return reverse_lazy(f'stations:{self.path_name}', args=(self.object.id,))

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(Station, pk=kwargs['pk'])
        if self.path_name == 'station_manager':
            if ((request.user != profile_user or not request.user.is_active)
                    and request.user.owner_id != profile_user.owner_id):
                raise Http404("User not found")
        elif self.path_name == 'station_owner':
            if (request.user != profile_user or not request.user.is_active) and profile_user.owner != request.user:
                raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)
