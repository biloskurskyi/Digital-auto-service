from django.contrib.auth import get_user_model

from cars.models import Car
from clients.models import Client
from core.services import tenant_of


def tenant_nav(request):
    user = getattr(request, 'user', None)
    if user is None or not user.is_authenticated:
        return {}
    tenant = tenant_of(user)
    nav = {
        'is_owner': user.owner_id is None,
        'clients': Client.objects.for_tenant(tenant),
        'cars': Car.objects.for_tenant(tenant),
    }
    if nav['is_owner']:
        nav['managers'] = get_user_model().objects.for_tenant(user)
    return {'nav': nav}
