from django.urls import path

from .views import CarCreateView, CarDeleteView, CarUpdateView

urlpatterns = [
    path('cars/new/', CarCreateView.as_view(), name='car_new'),
    path('cars/<int:pk>/edit/', CarUpdateView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]
