from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class StationQuerySet(models.QuerySet):
    def for_tenant(self, owner):
        return self.filter(owner=owner)


class Station(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StationQuerySet.as_manager()

    class Meta:
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'
        constraints = [
            models.UniqueConstraint(
                fields=('owner', 'name', 'address'),
                name='station_unique_owner_name_address',
                violation_error_message=_('Station with this name and address already exists.'),
            ),
        ]

    def __str__(self):
        return f'{self.name} on {self.address}'
