from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.views import View
from xhtml2pdf import pisa

from .services import company_report_context


class CompanyReportView(LoginRequiredMixin, View):
    def get(self, request):
        html = render_to_string('reports/company_report.html', company_report_context(request.user))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="company_report.pdf"'
        if pisa.CreatePDF(html, dest=response).err:
            return HttpResponseServerError()
        return response
