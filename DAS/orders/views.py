from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.views import View

from cars.models import Car
from common.views import OrderCreateView, OrderDeleteView, OrderUpdateView
from orders.models import Order
from workers.models import Worker


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
    paginate_by = 3

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     workers = Worker.objects.all()
    #     paginator = Paginator(workers, 3)  # 10 workers per page
    #     page = self.request.GET.get('page')
    #     try:
    #         workers = paginator.page(page)
    #     except PageNotAnInteger:
    #         workers = paginator.page(1)
    #     except EmptyPage:
    #         workers = paginator.page(paginator.num_pages)
    #     context['workers'] = workers
    #     return context

    # def get_workers_query(self):
    #     if self.creator_type == 'owner':
    #         owner = self.request.user if self.request.user.owner is None else self.request.user.owner
    #         return Worker.objects.filter(owner=owner)


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


# class GetWorkersForStationView(View):
#     def get(self, request, *args, **kwargs):
#         station_id = request.GET.get('station_id')
#         if station_id:
#             workers = Worker.objects.filter(station_id=station_id)
#             worker_choices = [(worker.id, str(worker), worker in request.user.workers.all()) for worker in workers]
#             print(JsonResponse({'worker_choices': worker_choices}))
#             return JsonResponse({'worker_choices': worker_choices})
#         return JsonResponse({'worker_choices': []})
