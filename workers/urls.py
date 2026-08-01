from django.urls import path

from .views import WorkerCreateView, WorkerDeleteView, WorkerUpdateView

urlpatterns = [
    path('workers/new/', WorkerCreateView.as_view(), name='worker_new'),
    path('workers/<int:pk>/edit/', WorkerUpdateView.as_view(), name='worker_edit'),
    path('workers/<int:pk>/delete/', WorkerDeleteView.as_view(), name='worker_delete'),
]
