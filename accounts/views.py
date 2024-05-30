from django.contrib import messages, auth
from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView

from accounts.forms import RegisterUserForm, LoginForm
from accounts.models import User, UserProfile
from vendor.forms import RegisterRestaurantForm


class UserRegistrationView(FormView):
    template_name = "accounts/register-user-page.html"
    form_class = RegisterUserForm
    success_url = "/accounts/registerUser/"

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect(reverse("dashboard"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(commit=False)
        userData = dict(**form.cleaned_data)
        userData.pop("confirm_password")
        user = User.objects.create_user(**userData)
        user.role = User.CUSTOMER
        user.save()
        messages.success(self.request, "Your account has been created!")
        return super().form_valid(form)


class RestaurantRegistrationView(View):
    def get(self, request):

        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect(reverse("dashboard"))

        user_form = RegisterUserForm()
        restaurant_form = RegisterRestaurantForm()
        return render(
            request,
            "accounts/register-restaurant-page.html",
            context={"uform": user_form, "rform": restaurant_form},
        )

    def post(self, request: HttpRequest):

        user_form = RegisterUserForm(request.POST)
        restaurant_form = RegisterRestaurantForm(request.POST, request.FILES)
        if user_form.is_valid() and restaurant_form.is_valid():
            userData = dict(**user_form.cleaned_data)
            userData.pop("confirm_password")
            user = User.objects.create_user(**userData)
            user.role = User.RESTAURANT
            user.save()
            vendor = restaurant_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
            messages.success(
                request, "Your account has been created! Please wait for the approval!"
            )
            return redirect(reverse("registerRestaurant"))
        return render(
            request,
            "accounts/register-restaurant-page.html",
            context={"uform": user_form, "rform": restaurant_form},
        )


class LoginView(FormView):
    template_name = "accounts/login-page.html"
    form_class = LoginForm
    success_url = "/accounts/dashboard/"

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect(reverse("dashboard"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                if user.check_password(password):
                    auth.login(self.request, user=user)
                    messages.success(self.request, "You are now logged in!")
                    return super().form_valid(form)
        form.add_error("email", "Invalid Credentials")
        messages.error(self.request, "Invalid Credentials")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "You have been logged out!")
        return redirect(reverse("login"))


class DashboardView(TemplateView):
    template_name = "accounts/dashboard-page.html"
