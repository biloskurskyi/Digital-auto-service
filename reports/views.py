from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View

from .services import PdfRenderer, PdfRenderError, company_report_context


class CompanyReportView(LoginRequiredMixin, View):
    renderer_class = PdfRenderer

    def get(self, request):
        try:
            pdf = self.renderer_class().render('reports/company_report.html', company_report_context(request.user))
        except PdfRenderError:
            return HttpResponse('Report is temporarily unavailable.', status=503, content_type='text/plain')
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="company_report.pdf"'
        return response
