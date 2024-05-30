from django.contrib import messages
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    # def get_context_data(self, **kwargs):
    #     if self.request.user.is_authenticated:
    #         messages.success(self.request, "you are logged in")
    #     return super().get_context_data(**kwargs)
