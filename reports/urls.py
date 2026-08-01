from django.urls import path

from .views import CompanyReportView

urlpatterns = [
    path('reports/company.pdf', CompanyReportView.as_view(), name='company_report'),
]
