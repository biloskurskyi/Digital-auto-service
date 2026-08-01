from datetime import date

from django.db import models

from cars.models import Car
from clients.models import Client
from stations.models import Station


class OrderQuerySet(models.QuerySet):
    def for_tenant(self, owner):
        return self.filter(client__owner=owner)


class Order(models.Model):
    class ProcessStatus(models.IntegerChoices):
        NOT_STARTED = 0, 'not started'
        IN_PROGRESS = 1, 'in progress'
        READY_FOR_PICKUP = 2, 'ready for pickup'
        PICKED_UP = 3, 'car picked up'

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    start_date = models.DateField(default=date.today)
    process_status = models.SmallIntegerField(choices=ProcessStatus.choices, default=ProcessStatus.NOT_STARTED)
    info = models.TextField(max_length=200)
    station = models.ForeignKey(Station, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.client} {self.car.car_number} {self.get_process_status_display()}'
