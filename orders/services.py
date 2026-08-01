from django.db import transaction


def save_order(form):
    with transaction.atomic():
        order = form.save()
        order.workers.set(form.cleaned_data['workers'])
    return order
