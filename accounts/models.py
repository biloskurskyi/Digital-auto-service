import uuid

from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserQuerySet(models.QuerySet):
    def for_tenant(self, owner):
        return self.filter(owner=owner)


class UserManager(DjangoUserManager.from_queryset(UserQuerySet)):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified_email', True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be a 10-digit number.')],
    )
    owner = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Email verification for {self.user.email}'
