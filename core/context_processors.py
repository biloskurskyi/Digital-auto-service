from django.contrib.auth import get_user_model


def tenant_nav(request):
    user = getattr(request, 'user', None)
    if user is None or not user.is_authenticated:
        return {}
    nav = {'is_owner': user.owner_id is None}
    if nav['is_owner']:
        nav['managers'] = get_user_model().objects.for_tenant(user)
    return {'nav': nav}
