from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from clients.models import Client


def validate_year_range(value):
    current_year = datetime.now().year
    # first_auto = 1886

    if value < 0 or value > current_year:
        raise ValidationError('Year must be between 1886 and 2024.')


class Car(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    car_number = models.CharField(max_length=8)
    vin_number = models.CharField(max_length=17)
    mark = models.CharField(max_length=16)
    model = models.CharField(max_length=32)
    year = models.IntegerField(validators=[validate_year_range])
    engine = models.CharField(max_length=32)
    gear_type = models.CharField(max_length=32)
    comment = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.car_number} {self.model} {self.mark}"
