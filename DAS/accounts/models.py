from django.contrib.auth.models import AbstractUser, User
from django.db import models


class AccountUsersManager(models.Manager):
    def get_managers(self, owner_id):
        managers = self.filter(owner_id=owner_id)
        user_info = [(user.username, user.id, user.first_name, user.last_name) for user in managers]
        return user_info

    def get_by_natural_key(self, username):
        return self.get(username=username)


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

    # def save(self, *args, **kwargs):
    #     is_creating_superuser = kwargs.pop('creating_superuser', False)
    #     if not self.is_superuser and is_creating_superuser:
    #         self.is_superuser = True
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"

    objects = AccountUsersManager()

    # def get_managers(self):
    #     managers = AccountUsers.objects.filter(owner=self.id)
    #     user_info = [(user.username, user.id, user.first_name, user.last_name) for user in managers]
    #     return user_info

# from accounts.models import AccountUsers
# >>> AccountsUsers.objects.get(username="DasAdmin2024").delete()
# Traceback (most recent call last):
#   File "<console>", line 1, in <module>
# NameError: name 'AccountsUsers' is not defined
# >>> AccountUsers.objects.get(username="DasAdmin2024").delete()
