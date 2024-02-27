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

import accounts
from accounts.forms import AccountProfileForm
from accounts.models import AccountUsers, EmailVerification
from cars.forms import CreateCarForm
from cars.models import Car
from clients.forms import ClientForm
from clients.models import Client
from orders.forms import CreateOrderForm, UpdateOrderForm
from orders.models import Order
from stations.forms import CreateStationForm
from stations.models import Station
from workers.forms import WorkerForm
from workers.models import Worker
from accounts.tasks import get_success_url
from django.core.cache import cache


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class CommonContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        managers = AccountUsers.objects.get_managers(self.request.user.id)
        context['managers'] = managers

        def cache_data(element_key, element_model, **kwargs):
            element = cache.get(element_key)
            if not element:
                element = element_model.objects.filter(**kwargs)
                cache.set(element_key, element, 30)
            return element

        if self.request.user.owner is not None:
            manager = get_object_or_404(AccountUsers, id=self.request.user.owner_id)

            # clients = cache.get('clients')
            # if not clients:
            #     context['clients'] = Client.objects.filter(owner=manager)
            #     cache.set('clients', context['clients'], 30)
            # else:
            #     context['clients'] = clients
            clients = cache_data('clients', Client, owner=manager)
            context['clients'] = clients

            cars = cache_data('cars', Car, client__owner=manager)
            context['cars'] = cars

            orders = cache_data('orders', Order, client__owner=manager)
            context['orders'] = orders

            stations = cache_data('stations', Station, owner=manager)
            context['stations'] = stations

            workers = cache_data('workers', Worker, owner=manager)
            context['workers'] = workers
            # clients = Client.objects.filter(owner=manager)
            # context['clients'] = [client for client in clients]
            # cars = Car.objects.filter(client__owner=manager)
            # context['cars'] = cars
            # orders = Order.objects.filter(client__owner=manager)
            # context['orders'] = orders
            # stations = Station.objects.filter(owner=manager)
            # context['stations'] = stations
            # workers = Worker.objects.filter(owner=manager)
            # context['workers'] = workers
        else:
            owner = get_object_or_404(AccountUsers, id=self.request.user.id)

            clients = cache_data('clients', Client, owner=owner)
            context['clients'] = clients

            cars = cache_data('cars', Car, client__owner=owner)
            context['cars'] = cars

            orders = cache_data('orders', Order, client__owner=owner)
            context['orders'] = orders

            stations = cache_data('stations', Station, owner=owner)
            context['stations'] = stations

            workers = cache_data('workers', Worker, owner=owner)
            context['workers'] = workers


            # clients = Client.objects.filter(owner=owner)
            # context['clients'] = [client for client in clients]
            # cars = Car.objects.filter(client__owner=owner)
            # context['cars'] = cars
            # orders = Order.objects.filter(client__owner=owner)
            # context['orders'] = orders
            # stations = Station.objects.filter(owner=owner)
            # context['stations'] = stations
            # workers = Worker.objects.filter(owner=owner)
            # context['workers'] = workers
        return context


class BaseView(TitleMixin, TemplateView):
    title = "DAS"


class CreateAccountView(TitleMixin, SuccessMessageMixin, CreateView):
    model = AccountUsers


class AccountProfileView(CommonContextMixin, TitleMixin, UpdateView):
    model = AccountUsers
    form_class = AccountProfileForm
    profile = 'profile'

    def get_success_url(self):
        success_url = get_success_url(self.profile, self.object.id)  # accounts.tasks.
        return success_url

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
    form_class = ClientForm
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


class ClientUpdateView(CommonContextMixin, TitleMixin, UpdateView):
    model = Client
    form_class = ClientForm
    form_invalid_info = 'Account was not deleted.'
    path_name = 'profile'
    title = 'client update'

    def get_success_url(self):
        messages.success(self.request, 'Client profile updated successfully.')
        return reverse_lazy(f'clients:{self.path_name}', args=(self.object.id,))

    def form_invalid(self, form):
        messages.error(self.request, 'Client profile wasn\'t updated')
        return super().form_invalid(form)

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


class CarUpdateView(CommonContextMixin, TitleMixin, UpdateView):
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
    title = "pdf report"
    template_name = 'accounts/pdf_clients.html'

    def get_context_data(self, **kwargs):
        context = {}

        if self.request.user.owner is not None:
            manager = get_object_or_404(AccountUsers, id=self.request.user.owner_id)
            managers = None
            clients = Client.objects.filter(owner=manager)
            cars = Car.objects.filter(client__owner=manager)
            workers = Worker.objects.filter(owner=manager)
            orders = Order.objects.filter(car__order__client__owner=manager)
            stations = None
        else:
            owner = get_object_or_404(AccountUsers, id=self.request.user.id)
            managers = AccountUsers.objects.filter(owner__isnull=False, owner=owner).distinct()
            clients = Client.objects.filter(owner=owner)
            cars = Car.objects.filter(client__owner=owner)
            workers = Worker.objects.filter(owner=owner)
            orders = Order.objects.filter(car__order__client__owner=owner)
            stations = Station.objects.filter(owner=self.request.user.id)
        context['managers'] = managers
        context['clients'] = clients
        context['cars'] = cars
        context['workers'] = workers
        context['orders'] = orders
        context['username'] = self.request.user.username
        context['stations'] = stations
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

        response = HttpResponse(content_type='application/pdf; charset=utf-8')
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


class OrderUpdateView(CommonContextMixin, TitleMixin, UpdateView):
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
            messages.success(self.request, 'Station created successfully.')
        elif self.path_name == 'owner_profile':
            owner_id = get_object_or_404(AccountUsers, id=self.request.user.id)
            form.instance.owner = owner_id
            messages.success(self.request, 'Station created successfully.')
        return super().form_valid(form)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class StationUpdateView(CommonContextMixin, TitleMixin, UpdateView):
    path_name = 'station'
    model = Station
    form_class = CreateStationForm
    title = 'station update'
    creator_type = 'manager'

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.object.owner.id  # Pass the owner to the form
        kwargs['username'] = self.request.user.id
        return kwargs


class WorkerCreateView(TitleMixin, CreateView):
    model = Worker
    form_class = WorkerForm
    path_name = 'profile'
    title = 'create worker'
    creator_type = ''

    def get_success_url(self):
        return reverse_lazy(f'accounts:{self.path_name}', args=(self.request.user.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs[self.creator_type] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        profile_user = get_object_or_404(AccountUsers, pk=kwargs['pk'])

        if not self.check_access(request, profile_user):
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.path_name == 'manager_profile':
            form.instance.owner = self.request.user.owner
            messages.success(self.request, 'Worker created successfully.')
        elif self.path_name == 'owner_profile':
            owner_id = get_object_or_404(AccountUsers, id=self.request.user.id)
            form.instance.owner = owner_id
            messages.success(self.request, 'Worker created successfully.')
        return super().form_valid(form)

    def check_access(self, request, profile_user):
        raise NotImplementedError("Subclasses must implement the check_access method")


class WorkerUpdateView(CommonContextMixin, TitleMixin, UpdateView):
    creator_type = ''
    reverse_page = path_name = ''

    form_valid_info = 'Worker was update successfully.'
    form_invalid_info = 'Worker was not updated.'
    model = Worker
    form_class = WorkerForm
    title = 'Worker update'

    def get_success_url(self):
        return reverse_lazy(f'workers:{self.reverse_page}', args=(self.object.id,))

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
        profile_user = get_object_or_404(Worker, pk=kwargs['pk'])
        if self.path_name == 'worker_manager':
            if ((request.user != profile_user or not request.user.is_active)
                    and request.user.owner_id != profile_user.owner_id):
                raise Http404("User not found")
        elif self.path_name == 'worker_owner':
            if ((request.user != profile_user or not request.user.is_active)
                    and profile_user.owner != request.user):
                raise Http404("User not found")
        else:
            raise Http404("User not found")
        return super().dispatch(request, *args, **kwargs)


class WorkerDeleteView(TitleMixin, DeleteView):
    form_valid_info = 'Worker deleted successfully.'
    form_invalid_info = 'Worker was not deleted.'
    reverse_page = ''
    model = Worker
    title = 'DAS - worker delete'

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
