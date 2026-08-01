from django.contrib import messages


class FlashMessagesMixin:
    success_message = ''
    error_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super().form_invalid(form)
