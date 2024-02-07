from datetime import date

from django.db import models
from django.utils import timezone

from cars.models import Car
from clients.models import Client


class Order(models.Model):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    READY_FOR_PICKUP = 2
    CAR_PIKED_UP = 3
    STATUSES = (
        (NOT_STARTED, 'not started'),
        (IN_PROGRESS, 'in progress'),
        (READY_FOR_PICKUP, 'ready for pickup'),
        (CAR_PIKED_UP, 'car picked up'),
    )

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    start_date = models.DateField(default=timezone.now)
    process_status = models.SmallIntegerField(default=NOT_STARTED, choices=STATUSES)
    info = models.TextField(max_length=200, default="repair")

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name} {self.car.car_number} {self.process_status}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
