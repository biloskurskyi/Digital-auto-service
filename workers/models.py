from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

from orders.models import Order


class WorkerQuerySet(models.QuerySet):
    def for_tenant(self, owner):
        return self.filter(owner=owner)


class Worker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField(validators=[MaxValueValidator(date.today)])
    years_of_experience = models.IntegerField()
    skills = models.TextField(max_length=200)
    salary = models.IntegerField()
    orders = models.ManyToManyField(Order, through='WorkerOrder', related_name='workers', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WorkerQuerySet.as_manager()

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class WorkerOrder(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('worker', 'order'), name='workerorder_unique_worker_order'),
        ]

    def __str__(self):
        return f'{self.worker} - {self.order}'
