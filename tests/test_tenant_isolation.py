import pytest
from django.urls import reverse

from accounts.models import User
from cars.models import Car
from clients.models import Client
from orders.models import Order
from stations.models import Station

from .factories import (
    ClientFactory,
    ManagerFactory,
    OrderFactory,
    OwnerFactory,
    StationFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def tenants():
    a, b = OwnerFactory(), OwnerFactory()
    order_a = OrderFactory(client=ClientFactory(owner=a))
    order_b = OrderFactory(client=ClientFactory(owner=b))
    return {
        'a': a, 'b': b,
        'station_a': StationFactory(owner=a), 'station_b': StationFactory(owner=b),
        'order_a': order_a, 'order_b': order_b,
    }


def test_for_tenant_selectors_return_only_own_records(tenants):
    a = tenants['a']
    assert list(Station.objects.for_tenant(a)) == [tenants['station_a']]
    assert list(Order.objects.for_tenant(a)) == [tenants['order_a']]
    assert list(Client.objects.for_tenant(a)) == [tenants['order_a'].client]
    assert list(Car.objects.for_tenant(a)) == [tenants['order_a'].car]


def test_manager_sees_owner_tenant_not_others(tenants):
    manager = ManagerFactory(owner=tenants['a'])
    assert list(Order.objects.for_tenant(tenants['a'])) == [tenants['order_a']]
    assert manager.owner_id == tenants['a'].pk


def test_owner_can_open_own_station(client, tenants):
    client.force_login(tenants['a'])
    response = client.get(reverse('station_edit', kwargs={'pk': tenants['station_a'].pk}))
    assert response.status_code == 200


def test_owner_gets_404_for_foreign_station(client, tenants):
    client.force_login(tenants['a'])
    response = client.get(reverse('station_edit', kwargs={'pk': tenants['station_b'].pk}))
    assert response.status_code == 404


def test_owner_gets_404_for_foreign_order(client, tenants):
    client.force_login(tenants['a'])
    response = client.get(reverse('order_edit', kwargs={'pk': tenants['order_b'].pk}))
    assert response.status_code == 404


def test_foreign_station_cannot_be_deleted(client, tenants):
    client.force_login(tenants['a'])
    response = client.post(reverse('station_delete', kwargs={'pk': tenants['station_b'].pk}))
    assert response.status_code == 404
    assert Station.objects.filter(pk=tenants['station_b'].pk).exists()


def test_manager_of_other_tenant_gets_404(client, tenants):
    manager_b = ManagerFactory(owner=tenants['b'])
    client.force_login(manager_b)
    response = client.get(reverse('order_edit', kwargs={'pk': tenants['order_a'].pk}))
    assert response.status_code == 404


def test_manager_cannot_create_station(client, tenants):
    client.force_login(ManagerFactory(owner=tenants['a']))
    assert client.get(reverse('station_new')).status_code == 404


def test_anonymous_is_redirected_to_login(client, tenants):
    response = client.get(reverse('station_edit', kwargs={'pk': tenants['station_a'].pk}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


def test_owner_cannot_edit_foreign_manager(client, tenants):
    foreign = ManagerFactory(owner=tenants['b'])
    client.force_login(tenants['a'])
    assert client.get(reverse('manager_edit', kwargs={'pk': foreign.pk})).status_code == 404


def test_invite_creates_manager_in_owner_tenant(client, tenants, mailoutbox):
    client.force_login(tenants['a'])
    response = client.post(reverse('manager_new'), {
        'username': 'newmanager', 'first_name': 'Max', 'last_name': 'Manager',
        'email': 'max@example.com', 'phone_number': '3000000001',
    })
    assert response.status_code == 302
    manager = User.objects.get(username='newmanager')
    assert manager.owner == tenants['a']
    assert not manager.has_usable_password()
    assert not manager.is_active
    assert len(mailoutbox) == 1
    assert 'max@example.com' in mailoutbox[0].to


def test_manager_cannot_invite_managers(client, tenants):
    client.force_login(ManagerFactory(owner=tenants['a']))
    assert client.post(reverse('manager_new'), {}).status_code == 404


def test_api_managers_list_is_tenant_scoped(api_client, tenants):
    mine = ManagerFactory(owner=tenants['a'])
    ManagerFactory(owner=tenants['b'])
    api_client.force_authenticate(tenants['a'])
    response = api_client.get('/api/managers/')
    assert response.status_code == 200
    assert [row['id'] for row in response.json()['results']] == [mine.pk]


def test_api_cannot_read_foreign_manager(api_client, tenants):
    foreign = ManagerFactory(owner=tenants['b'])
    api_client.force_authenticate(tenants['a'])
    assert api_client.get(f'/api/managers/{foreign.pk}/').status_code == 404


def test_api_create_binds_manager_to_owner(api_client, tenants):
    api_client.force_authenticate(tenants['a'])
    response = api_client.post('/api/managers/', {
        'username': 'apimgr', 'first_name': 'A', 'last_name': 'P',
        'email': 'api@example.com', 'phone_number': '3000000002',
    })
    assert response.status_code == 201
    assert User.objects.get(username='apimgr').owner == tenants['a']


def test_api_requires_authentication(api_client):
    assert api_client.get('/api/managers/').status_code == 401
