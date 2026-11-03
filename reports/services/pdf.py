import logging
from io import BytesIO

from django.template.loader import render_to_string
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)


class PdfRenderError(Exception):
    """Raised when a template cannot be rendered to PDF."""


class PdfRenderer:
    """Thin adapter over xhtml2pdf so views do not depend on pisa directly."""

    def render(self, template: str, context: dict) -> bytes:
        html = render_to_string(template, context)
        buffer = BytesIO()
        try:
            result = pisa.CreatePDF(html, dest=buffer)
        except Exception as exc:
            logger.exception('PDF rendering crashed for template %s', template)
            raise PdfRenderError(template) from exc
        if result.err:
            logger.error('PDF rendering failed for template %s (%s errors)', template, result.err)
            raise PdfRenderError(template)
        return buffer.getvalue()
