import pytest
from django.urls import reverse

from .factories import ClientFactory, ManagerFactory, OrderFactory, OwnerFactory

pytestmark = pytest.mark.django_db


def test_owner_gets_pdf_report(client):
    owner = OwnerFactory()
    OrderFactory(client=ClientFactory(owner=owner))
    client.force_login(owner)
    response = client.get(reverse('company_report'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'
    assert response.content.startswith(b'%PDF')


def test_manager_gets_pdf_report_for_own_tenant(client):
    manager = ManagerFactory()
    client.force_login(manager)
    response = client.get(reverse('company_report'))
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'


def test_report_does_not_leak_foreign_data(client):
    owner, other = OwnerFactory(), OwnerFactory()
    ClientFactory(owner=other, last_name='Foreignsurname')
    client.force_login(owner)
    from reports.services import company_report_context
    context = company_report_context(owner)
    assert not context['clients'].filter(last_name='Foreignsurname').exists()


def test_anonymous_cannot_get_report(client):
    response = client.get(reverse('company_report'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


def test_pdf_renderer_returns_bytes_from_pisa(monkeypatch):
    from reports.services import pdf

    class Ok:
        err = 0

    def fake_create(html, dest):
        dest.write(b'%PDF-fake')
        return Ok()

    monkeypatch.setattr(pdf.pisa, 'CreatePDF', fake_create)
    assert pdf.PdfRenderer().render('reports/company_report.html', {'username': 'u'}) == b'%PDF-fake'


def test_pdf_renderer_raises_on_pisa_error(monkeypatch):
    from reports.services import pdf

    class Bad:
        err = 1

    monkeypatch.setattr(pdf.pisa, 'CreatePDF', lambda html, dest: Bad())
    with pytest.raises(pdf.PdfRenderError):
        pdf.PdfRenderer().render('reports/company_report.html', {'username': 'u'})


def test_report_view_returns_503_when_render_fails(client, monkeypatch):
    from reports.services import pdf

    def boom(self, template, context):
        raise pdf.PdfRenderError(template)

    monkeypatch.setattr(pdf.PdfRenderer, 'render', boom)
    client.force_login(OwnerFactory())
    response = client.get(reverse('company_report'))
    assert response.status_code == 503


def test_user_is_owner_property():
    assert OwnerFactory().is_owner is True
    assert ManagerFactory().is_owner is False
