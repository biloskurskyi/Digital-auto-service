from django.contrib.auth.models import AbstractUser, User, UserManager
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext as _

from DAS import settings


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
    email = models.EmailField()  #
    phone_number = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey('AccountUsers', on_delete=models.PROTECT, null=True)
    is_verified_email = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     self.is_superuser = False
    #     if not self.is_active:
    #         existing_inactive_users = AccountUsers.objects.filter(email=self.email, is_active=False)
    #         if existing_inactive_users.exists():
    #             # Якщо неактивний користувач з таким емейлом існує, не перевіряти унікальність
    #             super().save(*args, **kwargs)
    #             return
    #     super().save(*args, **kwargs)

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

    # def save(self, *args, **kwargs):
    #     if not self.is_active:
    #         # Якщо користувач неактивний, встановити email на None, щоб уникнути перевірки унікальності
    #         self.email = None
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.is_active and not self.is_verified_email:
            self.is_verified_email = True
        self.is_superuser = False
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if not self.is_active:
    #         self.is_superuser = False
    #         super().save(*args, **kwargs)
    #     else:
    #         existing_active_user = AccountUsers.objects.filter(email=self.email, is_active=True).exists()
    #         if existing_active_user:
    #             raise ValueError("An active user with this email already exists.")
    #         else:
    #             self.is_superuser = False
    #             super().save(*args, **kwargs)


# @receiver(pre_save, sender=AccountUsers)
# def check_unique_email(sender, instance, **kwargs):
#     if instance.is_active and AccountUsers.objects.filter(email=instance.email, is_active=True).exists():
#         raise ValidationError("User with this email already exists")


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=AccountUsers, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email verification object for{self.user.email}'

    def send_verification_email(self):
        link = reverse('accounts:email_verification',
                       kwargs={'pk': self.user.pk, 'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'User confirmation {self.user.username}'
        message = 'To verify the identity of {}, follow the link: {}'.format(
            self.user.email,
            verification_link
        )

        password = self.user.password
        if self.user.owner is not None:
            message = 'Your password {}. To verify the identity of {}, follow the link: {}'.format(password,
                                                                                                   self.user.email,
                                                                                                   verification_link
                                                                                                   )

        send_mail(
            subject=subject,
            message=message,
            from_email='from@example.com',  # settings.EMAIL_HOST_USER
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    class Meta:
        verbose_name = "Email Verification Model"
        verbose_name_plural = "Email Verification Models"

    def is_expired(self):
        return (self.user.delete()) if now() >= self.expiration else False

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
