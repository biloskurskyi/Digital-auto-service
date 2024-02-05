from django.db import models

from cars.models import Car
from clients.models import Client


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name} {self.car.car_number}"
