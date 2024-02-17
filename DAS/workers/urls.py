from django.contrib.auth.decorators import login_required
from django.urls import path

from workers.views import (WorkerManagerCreateView, WorkerOwnerCreateView, )

app_name = 'workers'

urlpatterns = [
    path('owner/create/worker/profile/<int:pk>/', login_required(WorkerOwnerCreateView.as_view()),
         name='worker_owner_create'),
    path('manager/create/worker/profile/<int:pk>/', login_required(WorkerManagerCreateView.as_view()),
         name='worker_manager_create'),

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
