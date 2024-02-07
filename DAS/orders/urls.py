from django.contrib.auth.decorators import login_required
from django.urls import path

from orders.views import (GetCarsForClientView, OrderManagerCreateView,
                          OrderManagerDeleteView, OrderManagerUpdateView,
                          OrderOwnerCreateView, OrderOwnerDeleteView,
                          OrderOwnerUpdateView)

app_name = 'orders'

urlpatterns = [
    path('owner/create/order/profile/<int:pk>/', login_required(OrderOwnerCreateView.as_view()),
         name='order_owner_create'),
    path('manager/create/order/profile/<int:pk>/', login_required(OrderManagerCreateView.as_view()),
         name='order_manager_create'),

    path('owner/order/profile/<int:pk>/', login_required(OrderOwnerUpdateView.as_view()),
         name='order_owner'),
    path('manager/order/profile/<int:pk>/', login_required(OrderManagerUpdateView.as_view()),
         name='order_manager'),

    path('owner/delete/order/<int:pk>/', login_required(OrderOwnerDeleteView.as_view()),
         name='owner_delete_order'),
    path('manager/delete/order/<int:pk>/', login_required(OrderManagerDeleteView.as_view()),
         name='manager_delete_order'),

    path('get_cars_for_client/', login_required(GetCarsForClientView.as_view()),
         name='get_cars_for_client'),
]
