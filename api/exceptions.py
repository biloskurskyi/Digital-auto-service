from django.db.models import ProtectedError
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def protected_error_handler(exc, context):
    if isinstance(exc, ProtectedError):
        return Response(
            {'detail': _('This record cannot be deleted because other records depend on it.')},
            status=status.HTTP_409_CONFLICT,
        )
    return exception_handler(exc, context)
