from datetime import date

from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator
from django.db import models

from accounts.models import AccountUsers


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(validators=[MaxValueValidator(limit_value=date.today())])
    info = models.CharField(max_length=64)
    owner = models.ForeignKey(AccountUsers, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_all_cars(self):
        from cars.models import \
            Car  # Import inside the method to avoid circular import
        return Car.objects.filter(client=self)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
