from datetime import timedelta

from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext as _

from .models import EmailVerification, User

VERIFICATION_LIFETIME = timedelta(hours=24)


def register_owner(request, form):
    user = form.save()
    send_verification(request, user)
    return user


def send_verification(request, user):
    verification = EmailVerification.objects.create(user=user, expires_at=now() + VERIFICATION_LIFETIME)
    link = request.build_absolute_uri(
        reverse('verify', kwargs={'pk': user.pk, 'email': user.email, 'code': verification.code})
    )
    send_mail(
        subject=_('User confirmation %(username)s') % {'username': user.username},
        message=_('To verify the identity of %(email)s, follow the link: %(link)s') % {
            'email': user.email,
            'link': link,
        },
        from_email=None,
        recipient_list=[user.email],
    )


def verify_email(pk, email, code):
    EmailVerification.objects.filter(expires_at__lte=now()).delete()
    if User.objects.filter(email=email, is_verified_email=True).exists():
        return False
    user = User.objects.filter(pk=pk, email=email).first()
    if user is None:
        return False
    verification = EmailVerification.objects.filter(user=user, code=code, expires_at__gt=now()).first()
    if verification is None:
        return False
    with transaction.atomic():
        user.is_active = True
        user.is_verified_email = True
        user.save()
        EmailVerification.objects.filter(user=user).exclude(pk=verification.pk).update(expires_at=now())
        verification.delete()
    return True
