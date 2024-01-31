from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (ClientManagerCreateView, ClientManagerUpdateView,
                    ClientOwnerCreateView, ClientOwnerUpdateView,
                    CreateManagerView, IndexView, ManagerAccountDelete,
                    ManagerAccountProfileView, ManagerClientAccountDelete,
                    MianView, OwnerAccountDelete, OwnerAccountProfileView,
                    OwnerClientAccountDelete, OwnerManagerAccountProfileView,
                    UserLoginView, UserRegistrationView)

app_name = 'accounts'
urlpatterns = [
    path('', IndexView.as_view(), name='base'),

    path('registration/', UserRegistrationView.as_view(), name='reg'),
    path('login/', UserLoginView.as_view(), name='log'),
    path('success/login/', login_required(MianView.as_view()), name='success_log'),
    path('logout/', LogoutView.as_view(), name='log_out'),

    path('delete/owner/<int:pk>/', login_required(OwnerAccountDelete.as_view()), name='delete_owner'),
    path('delete/manager/<int:pk>/', login_required(ManagerAccountDelete.as_view()), name='delete_manager'),
    path('owner/delete/client/<int:pk>/', login_required(OwnerClientAccountDelete.as_view()),
         name='owner_delete_client'),
    path('manager/delete/client/<int:pk>/', login_required(ManagerClientAccountDelete.as_view()),
         name='manager_delete_client'),

    path('owner/profile/<int:pk>/', login_required(OwnerAccountProfileView.as_view()), name='owner_profile'),
    path('owner/manager/profile/<int:pk>/', login_required(OwnerManagerAccountProfileView.as_view()),
         name='owner_manager_profile'),
    path('manager/profile/<int:pk>/', login_required(ManagerAccountProfileView.as_view()), name='manager_profile'),
    path('create/manager/profile/<int:pk>/', login_required(CreateManagerView.as_view()), name='create_manager'),

    path('owner/create/client/profile/<int:pk>/', login_required(ClientOwnerCreateView.as_view()),
         name='client_owner_create'),
    path('manager/create/client/profile/<int:pk>/', login_required(ClientManagerCreateView.as_view()),
         name='manager_owner_create'),
    path('owner/client/profile/<int:pk>/', login_required(ClientOwnerUpdateView.as_view()),
         name='client_owner'),
    path('manager/client/profile/<int:pk>/', login_required(ClientManagerUpdateView.as_view()),
         name='client_manager'),

]
