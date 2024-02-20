from django.contrib.auth.models import AbstractUser, User, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext as _


class AccountUsersManager(UserManager):
    def get_managers(self, owner_id):
        managers = self.filter(owner_id=owner_id)
        user_info = [(user.username, user.id, user.first_name, user.last_name) for user in managers]
        return user_info

    def get_by_natural_key(self, username):
        return self.get(username=username)

    def normalize_email(self, email):
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email


class AccountUsers(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey('AccountUsers', on_delete=models.PROTECT, null=True)

    def save(self, *args, **kwargs):
        self.is_superuser = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    objects = AccountUsersManager()

    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'
                    ),
    )

    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     verbose_name='groups',
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     related_name='owner_users_groups'
    # )
    #

    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     verbose_name='user permissions',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     related_name='owner_users_permissions'
    # )
    # def save(self, *args, **kwargs):
    #     is_creating_superuser = kwargs.pop('creating_superuser', False)
    #     if not self.is_superuser and is_creating_superuser:
    #         self.is_superuser = True
    #     super().save(*args, **kwargs)

    # def get_managers(self):
    #     managers = AccountUsers.objects.filter(owner=self.id)
    #     user_info = [(user.username, user.id, user.first_name, user.last_name) for user in managers]
    #     return user_info


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=AccountUsers, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email verification object for{self.user.email}'

    def send_verification_email(self):
        send_mail(
            "Subject here",
            "Test verification email.",
            "from@example.com",
            [self.user.email],
            fail_silently=False,
        )

    class Meta:
        verbose_name = "Email Verification Model"
        verbose_name_plural = "Email Verification Models"
