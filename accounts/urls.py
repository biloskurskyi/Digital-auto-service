from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    AccountDeleteView, DashboardView, LandingView, LoginSuccessView, LoginView, ManagerCreateView, ManagerDeleteView,
    ManagerUpdateView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView,
    RegisterView, VerifyInvalidView, VerifySentView, VerifyView,
)

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/success/', LoginSuccessView.as_view(), name='login_success'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/sent/', VerifySentView.as_view(), name='verify_sent'),
    path('verify/invalid/', VerifyInvalidView.as_view(), name='verify_invalid'),
    path('verify/<int:pk>/<str:email>/<uuid:code>/', VerifyView.as_view(), name='verify'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('account/delete/', AccountDeleteView.as_view(), name='account_delete'),
    path('managers/new/', ManagerCreateView.as_view(), name='manager_new'),
    path('managers/<int:pk>/edit/', ManagerUpdateView.as_view(), name='manager_edit'),
    path('managers/<int:pk>/delete/', ManagerDeleteView.as_view(), name='manager_delete'),
]
