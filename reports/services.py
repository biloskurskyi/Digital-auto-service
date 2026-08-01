from django.contrib.auth import get_user_model

from cars.models import Car
from clients.models import Client
from core.services import tenant_of
from orders.models import Order
from stations.models import Station
from workers.models import Worker


def company_report_context(user):
    tenant = tenant_of(user)
    is_owner = user.owner_id is None
    return {
        'username': user.username,
        'managers': get_user_model().objects.for_tenant(user) if is_owner else None,
        'clients': Client.objects.for_tenant(tenant),
        'cars': Car.objects.for_tenant(tenant).select_related('client'),
        'workers': Worker.objects.for_tenant(tenant).prefetch_related('orders__client', 'orders__car'),
        'orders': Order.objects.for_tenant(tenant).select_related('client', 'car', 'station')
                       .prefetch_related('workers'),
        'stations': Station.objects.for_tenant(tenant) if is_owner else None,
    }
