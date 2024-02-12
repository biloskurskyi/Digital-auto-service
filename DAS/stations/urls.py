from django.contrib.auth.decorators import login_required
from django.urls import path

from stations.views import StationOwnerCreateView, StationManagerCreateView, StationOwnerUpdateView, \
    StationManagerUpdateView, StationDeleteView

app_name = 'stations'

urlpatterns = [
    path('owner/create/station/profile/<int:pk>/', login_required(StationOwnerCreateView.as_view()),
         name='station_owner_create'),
    path('manager/create/station/profile/<int:pk>/', login_required(StationManagerCreateView.as_view()),
         name='station_manager_create'),

    path('owner/station/profile/<int:pk>/', login_required(StationOwnerUpdateView.as_view()),
         name='station_owner'),
    path('manager/station/profile/<int:pk>/', login_required(StationManagerUpdateView.as_view()),
         name='station_manager'),

    path('owner/delete/station/<int:pk>/', login_required(StationDeleteView.as_view()),
         name='owner_delete_station'),
]
