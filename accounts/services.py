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


def invite_manager(request, form, owner):
    user = form.save(commit=False)
    user.owner = owner
    user.set_unusable_password()
    user.save()
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


def pending_verification(pk, email, code):
    EmailVerification.objects.filter(expires_at__lte=now()).delete()
    if User.objects.filter(email=email, is_verified_email=True).exists():
        return None
    user = User.objects.filter(pk=pk, email=email).first()
    if user is None:
        return None
    return EmailVerification.objects.filter(user=user, code=code, expires_at__gt=now()).select_related('user').first()


def complete_verification(verification):
    user = verification.user
    with transaction.atomic():
        user.is_active = True
        user.is_verified_email = True
        user.save()
        EmailVerification.objects.filter(user=user).exclude(pk=verification.pk).update(expires_at=now())
        verification.delete()


def activate_manager(verification, password_form):
    with transaction.atomic():
        password_form.save()
        complete_verification(verification)
