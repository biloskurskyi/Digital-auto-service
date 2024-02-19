from django.contrib.auth.decorators import login_required
from django.urls import path

from workers.views import (WorkerManagerCreateView, WorkerOwnerCreateView, WorkerOwnerUpdateView,
                           WorkerManagerUpdateView, WorkerOwnerDeleteView, WorkerManagerDeleteView)

app_name = 'workers'

urlpatterns = [
    path('owner/create/worker/profile/<int:pk>/', login_required(WorkerOwnerCreateView.as_view()),
         name='worker_owner_create'),
    path('manager/create/worker/profile/<int:pk>/', login_required(WorkerManagerCreateView.as_view()),
         name='worker_manager_create'),

    path('owner/worker/profile/<int:pk>/', login_required(WorkerOwnerUpdateView.as_view()),
         name='worker_owner'),
    path('manager/worker/profile/<int:pk>/', login_required(WorkerManagerUpdateView.as_view()),
         name='worker_manager'),

    path('owner/delete/worker/<int:pk>/', login_required(WorkerOwnerDeleteView.as_view()),
         name='owner_delete_worker'),
    path('manager/delete/worker/<int:pk>/', login_required(WorkerManagerDeleteView.as_view()),
         name='manager_delete_worker'),

    # path('owner/order/profile/<int:pk>/', login_required(OrderOwnerUpdateView.as_view()),
    #      name='worker_owner'),
    # path('manager/order/profile/<int:pk>/', login_required(OrderManagerUpdateView.as_view()),
    #      name='worker_manager'),
    #
    # path('owner/delete/order/<int:pk>/', login_required(OrderOwnerDeleteView.as_view()),
    #      name='owner_delete_worker'),
    # path('manager/delete/order/<int:pk>/', login_required(OrderManagerDeleteView.as_view()),
    #      name='manager_delete_worker'),

]
