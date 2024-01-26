from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, CreateView

from accounts.models import AccountUsers


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class BaseView(TitleMixin, TemplateView):
    title = "DAS"


class CreateAccountView(TitleMixin, SuccessMessageMixin, CreateView):
    model = AccountUsers
