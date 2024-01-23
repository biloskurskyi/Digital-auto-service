from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', UserRegistrationView.as_view(), name='reg'),
    path('login/', UserLoginView.as_view(), name='log'),
    path('ok/', login_required(OkView.as_view()), name='ok'),
]
