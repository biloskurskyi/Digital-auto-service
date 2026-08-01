from django.urls import path

from .views import ClientCarsView, OrderCreateView, OrderDeleteView, OrderUpdateView

urlpatterns = [
    path('orders/new/', OrderCreateView.as_view(), name='order_new'),
    path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_edit'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('clients/<int:pk>/cars/', ClientCarsView.as_view(), name='client_cars'),
]
