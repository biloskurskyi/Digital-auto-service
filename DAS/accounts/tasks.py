from celery import shared_task
from django.urls import reverse_lazy
from django.utils.timezone import now

from accounts.models import EmailVerification


@shared_task
def get_success_url(profile, object_id):
    return reverse_lazy(f'accounts:{profile}', args=(object_id,))


# @shared_task
# def check_expired_tokens():
#     expired_tokens = EmailVerification.objects.filter(expiration__lte=now())
#     for token in expired_tokens:
#         token.delete()


