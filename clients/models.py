from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models


class ClientQuerySet(models.QuerySet):
    def for_tenant(self, owner):
        return self.filter(owner=owner)


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(validators=[MaxValueValidator(date.today)])
    info = models.CharField(max_length=64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ClientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
