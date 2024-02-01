from django.contrib.auth.decorators import login_required
from django.urls import path

from cars.views import CarOwnerCreateView, CarManagerCreateView, CarOwnerUpdateView, CarManagerUpdateView, \
    OwnerCarAccountDelete, ManagerCarAccountDelete

app_name = 'cars'

urlpatterns = [
    path('owner/create/car/profile/<int:pk>/', login_required(CarOwnerCreateView.as_view()),
         name='car_owner_create'),
    path('manager/create/car/profile/<int:pk>/', login_required(CarManagerCreateView.as_view()),
         name='car_manager_create'),

    path('owner/car/profile/<int:pk>/', login_required(CarOwnerUpdateView.as_view()),
         name='car_owner'),
    path('manager/car/profile/<int:pk>/', login_required(CarManagerUpdateView.as_view()),
         name='car_manager'),

    path('owner/delete/car/<int:pk>/', login_required(OwnerCarAccountDelete.as_view()),
         name='owner_delete_car'),
    path('manager/delete/car/<int:pk>/', login_required(ManagerCarAccountDelete.as_view()),
         name='manager_delete_car'),
]
