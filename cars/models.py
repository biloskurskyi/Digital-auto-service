from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from clients.models import Client

FIRST_CAR_YEAR = 1886


def current_year():
    return date.today().year


class CarQuerySet(models.QuerySet):
    def for_tenant(self, owner):
        return self.filter(client__owner=owner)


class Car(models.Model):
    class GearType(models.IntegerChoices):
        BEVEL = 0, 'bevel gears'
        WORM = 1, 'worm gears'
        HELICAL = 2, 'helical gears'
        RACK_AND_PINION = 3, 'rack and pinion gears'
        INTERNAL = 4, 'internal gears'
        STRAIGHT_BEVEL = 5, 'straight bevel gears'
        SPIRAL_BEVEL = 6, 'spiral bevel gears'
        DOUBLE_HELICAL = 7, 'double helical gears'
        CROWN = 8, 'crown gears'
        HERRINGBONE = 9, 'herringbone gears'
        ANOTHER = 10, 'another type'

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    car_number = models.CharField(max_length=8)
    vin_number = models.CharField(max_length=17)
    mark = models.CharField(max_length=16)
    model = models.CharField(max_length=32)
    year = models.IntegerField(validators=[MinValueValidator(FIRST_CAR_YEAR), MaxValueValidator(current_year)])
    engine = models.CharField(max_length=32)
    gear_type = models.SmallIntegerField(choices=GearType.choices, default=GearType.ANOTHER)
    comment = models.TextField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CarQuerySet.as_manager()

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f'{self.car_number} {self.model} {self.mark}'
