from datetime import date

from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator
from django.db import models
from django.shortcuts import get_object_or_404


class AccountUsers(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey('AccountUsers', on_delete=models.PROTECT, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='owner_users_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='owner_users_permissions'
    )

    def save(self, *args, **kwargs):
        self.is_superuser = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"

    def get_managers(self):
        managers = AccountUsers.objects.filter(owner=self.id)
        user_info = [(user.username, user.id) for user in managers]
        return user_info


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(validators=[MaxValueValidator(limit_value=date.today())])
    type = models.CharField(max_length=16)
    owner = models.ForeignKey('AccountUsers', on_delete=models.PROTECT, null=True)
