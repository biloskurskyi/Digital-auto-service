import factory

from accounts.models import User
from cars.models import Car
from clients.models import Client
from orders.models import Order
from stations.models import Station

PASSWORD = 'pass12345!'


class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f'owner{n}')
    first_name = 'Olga'
    last_name = 'Owner'
    email = factory.Sequence(lambda n: f'owner{n}@example.com')
    phone_number = factory.Sequence(lambda n: f'{1000000000 + n}')
    is_active = True
    is_verified_email = True
    password = factory.PostGenerationMethodCall('set_password', PASSWORD)

    @factory.post_generation
    def _save_password(self, create, extracted, **kwargs):
        if create:
            self.save()


class ManagerFactory(OwnerFactory):
    username = factory.Sequence(lambda n: f'manager{n}')
    email = factory.Sequence(lambda n: f'manager{n}@example.com')
    phone_number = factory.Sequence(lambda n: f'{2000000000 + n}')
    owner = factory.SubFactory(OwnerFactory)


class StationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Station

    name = factory.Sequence(lambda n: f'Station {n}')
    address = factory.Sequence(lambda n: f'Street {n}')
    owner = factory.SubFactory(OwnerFactory)


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    first_name = 'Ivan'
    last_name = 'Client'
    email = factory.Sequence(lambda n: f'client{n}@example.com')
    phone_number = '0501234567'
    date_of_birth = '1990-01-01'
    info = 'regular'
    owner = factory.SubFactory(OwnerFactory)


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    client = factory.SubFactory(ClientFactory)
    car_number = factory.Sequence(lambda n: f'AA{n:04d}')
    vin_number = factory.Sequence(lambda n: f'VIN{n:014d}')
    mark = 'Skoda'
    model = 'Octavia'
    year = 2015
    engine = '1.6'
    comment = 'ok'


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    client = factory.SubFactory(ClientFactory)
    car = factory.SubFactory(CarFactory, client=factory.SelfAttribute('..client'))
    info = 'oil change'
