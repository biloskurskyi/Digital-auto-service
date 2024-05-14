from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (CreateManagerView, EmailMessageView, EmailNotVerified,
                    EmailVerificationView, IndexView, ManagerAccountDelete,
                    ManagerAccountProfileView, ManagerGeneratePDFView,
                    MianView, OwnerAccountDelete, OwnerAccountProfileView,
                    OwnerGeneratePDFView, OwnerManagerAccountProfileView,
                    UserLoginView, UserRegistrationView)

app_name = 'accounts'
urlpatterns = [
    path('', IndexView.as_view(), name='base'),

    path('registration/', UserRegistrationView.as_view(), name='reg'),
    path('login/', UserLoginView.as_view(), name='log'),
    path('success/login/', login_required(MianView.as_view()), name='success_log'),
    path('logout/', LogoutView.as_view(), name='log_out'),

    path('delete/owner/<int:pk>/', login_required(OwnerAccountDelete.as_view()), name='delete_owner'),
    path('delete/manager/<int:pk>/', login_required(ManagerAccountDelete.as_view()), name='delete_manager'),

    path('owner/profile/<int:pk>/', login_required(OwnerAccountProfileView.as_view()),
         name='owner_profile'),
    # path('owner/profile/<int:pk>/', cache_page(30)(login_required(OwnerAccountProfileView.as_view())),
    #      name='owner_profile'),
    path('owner/manager/profile/<int:pk>/', login_required(OwnerManagerAccountProfileView.as_view()),
         name='owner_manager_profile'),
    path('manager/profile/<int:pk>/', login_required(ManagerAccountProfileView.as_view()), name='manager_profile'),
    path('create/manager/profile/<int:pk>/', login_required(CreateManagerView.as_view()), name='create_manager'),

    path('owner/generate_pdf/<int:pk>/', login_required(OwnerGeneratePDFView.as_view()), name='owner_generate_pdf'),
    #     http://localhost:8009/generate_pdf/131/
    path('manager/generate_pdf/<int:pk>/', login_required(ManagerGeneratePDFView.as_view()),
         name='manager_generate_pdf'),

    path('verify/<int:pk>/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),
    path('notverify/', EmailNotVerified.as_view(), name='email_not_verified'),
    path('verify/', EmailMessageView.as_view(), name='email_message')

]
