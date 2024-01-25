from django.contrib.auth.models import AbstractUser, User
from django.db import models


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

#
# class AccountManagersUsers(AbstractUser):
#     first_name = models.CharField(max_length=32)
#     last_name = models.CharField(max_length=32)
#     username = models.CharField(max_length=32, unique=True)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     owner = models.ForeignKey('AccountOwnerUsers', on_delete=models.PROTECT)
#
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to.',
#         related_name='managers_users_groups'
#     )
#
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name='managers_users_permissions'
#     )
#
#     class Meta:
#         verbose_name_plural = "Managers"
