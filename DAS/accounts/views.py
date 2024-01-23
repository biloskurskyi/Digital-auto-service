from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
# from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CreateAccountUserForm, UserLoginForm
from .models import AccountUsers


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = AccountUsers
    form_class = CreateAccountUserForm
    template_name = 'accounts/registration.html'
    success_message = 'Registration is successfully done!'
    title = 'DAS - registration'
    success_url = reverse_lazy('accounts:log')


class UserLoginView(TitleMixin, LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    title = 'DAS - login'


class OkView(TemplateView):
    template_name = "accounts/successful_page.html"
