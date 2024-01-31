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
    type = models.CharField(max_length=16)
    owner = models.ForeignKey(AccountUsers, on_delete=models.PROTECT, null=True)
