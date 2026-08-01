from django.urls import path

from .views import ClientCreateView, ClientDeleteView, ClientUpdateView

urlpatterns = [
    path('clients/new/', ClientCreateView.as_view(), name='client_new'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]
