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
    BEVEL_GEARS = 0
    WORM_GEARS = 1
    HELICAL_GEARS = 2
    RACK_AND_PINION_GEARS = 3
    INTERNAL_GEARS = 4
    STRAIGHT_BEVEL_GEARS = 5
    SPIRAL_BEVEL_GEARS = 6
    DOUBLE_HELICAL_GEARS = 7
    CROWN_GEARS = 8
    HERRINGBONE_GEARS = 9
    ANOTHER_TYPE = 10
    STATUSES = (
        (BEVEL_GEARS, 'bevel gears'),
        (WORM_GEARS, 'worm gears'),
        (HELICAL_GEARS, 'helical gears'),
        (RACK_AND_PINION_GEARS, 'rack and pinion gears'),
        (INTERNAL_GEARS, 'internal gears'),
        (STRAIGHT_BEVEL_GEARS, 'straight bevel gears'),
        (SPIRAL_BEVEL_GEARS, 'spiral bevel gears'),
        (DOUBLE_HELICAL_GEARS, 'double helical gears'),
        (CROWN_GEARS, 'crown gears'),
        (HERRINGBONE_GEARS, 'herringbone gears'),
        (ANOTHER_TYPE, 'another type'),
    )

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    car_number = models.CharField(max_length=8)
    vin_number = models.CharField(max_length=17)
    mark = models.CharField(max_length=16)
    model = models.CharField(max_length=32)
    year = models.IntegerField(validators=[validate_year_range])
    engine = models.CharField(max_length=32)
    # gear_type = models.CharField(max_length=32)
    gear_type = models.SmallIntegerField(default=ANOTHER_TYPE, choices=STATUSES)
    comment = models.TextField(max_length=60)

    def __str__(self):
        return f"{self.car_number} {self.model} {self.mark}"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
