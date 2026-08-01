from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = 'accounts/landing.html'
    extra_context = {'title': 'DAS'}
