from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (ClientManagerCreateView, ClientManagerUpdateView,
                    ClientOwnerCreateView, ClientOwnerUpdateView,
                    ManagerClientAccountDelete, OwnerClientAccountDelete)

app_name = 'clients'

urlpatterns = [
    path('owner/delete/client/<int:pk>/', login_required(OwnerClientAccountDelete.as_view()),
         name='owner_delete_client'),
    path('manager/delete/client/<int:pk>/', login_required(ManagerClientAccountDelete.as_view()),
         name='manager_delete_client'),

    path('owner/create/client/profile/<int:pk>/', login_required(ClientOwnerCreateView.as_view()),
         name='client_owner_create'),
    path('manager/create/client/profile/<int:pk>/', login_required(ClientManagerCreateView.as_view()),
         name='client_manager_create'),

    path('owner/client/profile/<int:pk>/', login_required(ClientOwnerUpdateView.as_view()),
         name='client_owner'),
    path('manager/client/profile/<int:pk>/', login_required(ClientManagerUpdateView.as_view()),
         name='client_manager'),
]
