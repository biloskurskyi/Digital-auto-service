from celery import shared_task
from django.urls import reverse_lazy


@shared_task
def get_success_url(profile, object_id):
    return reverse_lazy(f'accounts:{profile}', args=(object_id,))


