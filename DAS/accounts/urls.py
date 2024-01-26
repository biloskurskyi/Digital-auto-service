from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (OwnerAccountProfileView, IndexView, MianView, UserLoginView, UserRegistrationView, AccountDelete,
                    OwnerManagerAccountProfileView, ManagerAccountProfileView, CreateManagerView)

app_name = 'accounts'
urlpatterns = [
    path('', IndexView.as_view(), name='base'),

    path('registration/', UserRegistrationView.as_view(), name='reg'),
    path('login/', UserLoginView.as_view(), name='log'),
    path('success/login/', login_required(MianView.as_view()), name='success_log'),
    path('logout/', LogoutView.as_view(), name='log_out'),

    path('delete/<int:pk>/', login_required(AccountDelete.as_view()), name='delete'),

    path('owner/profile/<int:pk>/', login_required(OwnerAccountProfileView.as_view()), name='owner_profile'),
    path('owner/manager/profile/<int:pk>/', login_required(OwnerManagerAccountProfileView.as_view()),
         name='owner_manager_profile'),
    path('manager/profile/<int:pk>/', login_required(ManagerAccountProfileView.as_view()), name='manager_profile'),
    path('create/manager/profile/<int:pk>/', login_required(CreateManagerView.as_view()), name='create_manager'),

]
