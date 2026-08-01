from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class ProtectedErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ProtectedError):
            messages.error(request, _('This record cannot be deleted because other records depend on it.'))
            return redirect(request.path)
        return None
