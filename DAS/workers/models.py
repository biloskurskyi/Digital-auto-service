from django.db import models

from accounts.models import AccountUsers
from orders.models import Order
from stations.models import Station


class Worker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    years_of_experience = models.IntegerField()
    skills = models.TextField(max_length=200, default="")
    salary = models.IntegerField()
    orders = models.ManyToManyField('orders.Order', through='workers.WorkerOrder')
    owner = models.ForeignKey(AccountUsers, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"


class WorkerOrder(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.worker} - {self.order}"
