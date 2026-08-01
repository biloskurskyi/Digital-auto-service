from django.urls import path

from .views import StationCreateView, StationDeleteView, StationUpdateView

urlpatterns = [
    path('stations/new/', StationCreateView.as_view(), name='station_new'),
    path('stations/<int:pk>/edit/', StationUpdateView.as_view(), name='station_edit'),
    path('stations/<int:pk>/delete/', StationDeleteView.as_view(), name='station_delete'),
]
