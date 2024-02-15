from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import AccountUsers


class Station(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=32, null=True)
    owner = models.ForeignKey(AccountUsers, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.name} on {self.address}"

    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Stations"
        unique_together = ('name', 'address',)

    def clean(self):
        existing_stations = Station.objects.filter(name=self.name, address=self.address)
        if self.pk:
            existing_stations = existing_stations.exclude(pk=self.pk)

    # def get_owned_stations(user):
    #     return Station.objects.filter(owner_id=user.id)
