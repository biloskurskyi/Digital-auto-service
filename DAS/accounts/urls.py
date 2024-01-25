from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (AccountProfile, IndexView, MianView, UserLoginView, UserRegistrationView, AccountDelete)

app_name = 'accounts'
urlpatterns = [
    path('', IndexView.as_view(), name='base'),
    path('registration/', UserRegistrationView.as_view(), name='reg'),
    path('login/', UserLoginView.as_view(), name='log'),
    path('delete/<int:pk>/', login_required(AccountDelete.as_view()), name='delete'),
    path('succeslogin/', login_required(MianView.as_view()), name='success_log'),
    path('profile/<int:pk>/', login_required(AccountProfile.as_view()), name='ok'),
]
