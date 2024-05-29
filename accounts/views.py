from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, FormView

from accounts.forms import RegisterForm
from accounts.models import User


class UserRegistrationView(FormView):
    template_name = "accounts/register-user-page.html"
    form_class = RegisterForm
    success_url = "/accounts/registerUser/"

    def form_valid(self, form):
        form.save(commit=False)
        userData = dict(**form.cleaned_data)
        userData.pop("confirm_password")
        user = User.objects.create_user(**userData)
        user.role = User.CUSTOMER
        user.save()
        messages.success(self.request, "Your account has been created!")
        return super().form_valid(form)
