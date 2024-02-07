from django.http import JsonResponse
from django.views import View

from cars.models import Car
from common.views import OrderCreateView, OrderDeleteView, OrderUpdateView
from orders.models import Order


class OrderOwnerCreateView(OrderCreateView):
    reverse_page = 'owner_profile'
    creator_type = 'owner'
    template_name = 'orders/owner_create_order.html'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is None


class OrderManagerCreateView(OrderCreateView):
    reverse_page = 'manager_profile'
    creator_type = 'manager'
    template_name = 'orders/manager_create_order.html'

    def check_access(self, request, profile_user):
        return request.user == profile_user and request.user.is_active and request.user.owner is not None


class OrderOwnerUpdateView(OrderUpdateView):
    template_name = 'orders/owner_order.html'
    creator_type = 'owner'
    reverse_page = path_name = 'order_owner'


class OrderManagerUpdateView(OrderUpdateView):
    template_name = 'orders/manager_order.html'
    creator_type = 'manager'
    reverse_page = path_name = 'order_manager'


class OrderOwnerDeleteView(OrderDeleteView):
    template_name = 'orders/owner_delete_order.html'
    reverse_page = 'owner_profile'

    def check_access(self, request, profile_user):
        return request.user == profile_user.client.owner


class OrderManagerDeleteView(OrderDeleteView):
    template_name = 'orders/manager_delete_order.html'
    reverse_page = 'manager_profile'

    def check_access(self, request, profile_user):
        return profile_user.client.owner == request.user.owner


class GetCarsForClientView(View):
    def get(self, request, *args, **kwargs):
        client_id = request.GET.get('client_id')
        if client_id:
            cars = Car.objects.filter(client_id=client_id)
            car_choices = [(car.id, str(car)) for car in cars]

            return JsonResponse({'car_choices': car_choices}, )
        return JsonResponse({'car_choices': []})
