from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView

from accounts.forms import RegisterUserForm
from accounts.models import User, UserProfile
from vendor.forms import RegisterRestaurantForm


class UserRegistrationView(FormView):
    template_name = "accounts/register-user-page.html"
    form_class = RegisterUserForm
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


class RestaurantRegistrationView(View):
    def get(self, request):
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
