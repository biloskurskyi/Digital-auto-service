import pytest
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def _locmem_email(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


@pytest.fixture(autouse=True)
def _insecure_cookies(settings):
    # pytest-django forces DEBUG=False, which would make session cookies Secure-only
    settings.SESSION_COOKIE_SECURE = False
    settings.CSRF_COOKIE_SECURE = False


@pytest.fixture(autouse=True)
def _no_throttle(settings):
    settings.REST_FRAMEWORK = {
        **settings.REST_FRAMEWORK,
        'DEFAULT_THROTTLE_CLASSES': [],
    }


@pytest.fixture
def api_client():
    return APIClient()
