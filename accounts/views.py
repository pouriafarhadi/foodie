from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from accounts.forms import RegisterUserForm, LoginForm, ResetPasswordForm
from accounts.models import User, UserProfile
from accounts.utils import detectUser, send_mail, checkIfItsCustomer, checkIfItsVendor
from vendor.forms import RegisterRestaurantForm


class UserRegistrationView(FormView):
    template_name = "accounts/register-user-page.html"
    form_class = RegisterUserForm
    success_url = "/registerUser/"

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect(reverse("my-Account"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(commit=False)
        userData = dict(**form.cleaned_data)
        userData.pop("confirm_password")
        user = User.objects.create_user(**userData)
        user.role = User.CUSTOMER
        user.save()
        # send verification email
        mail_subject = "Activation Account"
        email_template = "accounts/emails/account-verification-mail.html"
        send_mail(self.request, user, mail_subject, email_template)
        messages.success(self.request, "Your account has been created!")
        return super().form_valid(form)


class RestaurantRegistrationView(View):
    def get(self, request):

        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect(reverse("my-Account"))

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
            # send verification email
            mail_subject = "Activation Account"
            email_template = "accounts/emails/account-verification-mail.html"
            send_mail(self.request, user, mail_subject, email_template)
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
    success_url = "/myAccount/"

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect(reverse("my-Account"))
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
        messages.warning(self.request, "Invalid Credentials")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "You have been logged out!")
        return redirect(reverse("login"))


class VendorDashboard(TemplateView):
    template_name = "accounts/vendorDashboard.html"

    def get(self, request, *args, **kwargs):
        # check if specific role want to see another role dashboard
        checkIfItsVendor(request)
        return super().get(request, *args, **kwargs)


class CustDashboard(TemplateView):
    template_name = "accounts/custDashboard.html"

    def get(self, request, *args, **kwargs):
        checkIfItsCustomer(request)
        return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     context["user"] = user


class myAccount(View):
    def get(self, request):
        user = request.user
        redirectUrl = detectUser(user)
        return redirect(reverse(redirectUrl))


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated!")
        return redirect(reverse("my-Account"))
    else:
        messages.warning(request, "Invalid activation link")
        return redirect(reverse("my-Account"))


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # send reset password email
            mail_subject = "Reset Your Password"
            email_template = "accounts/emails/reset-password-mail.html"
            send_mail(request, user, mail_subject, email_template)
            messages.success(
                request, "password reset link has been sent to your email address"
            )
            return redirect(reverse("login"))
        else:
            messages.warning(request, "Email doesn't exist!")
    return render(request, "accounts/forgot-password-page.html")


def reset_password_validate(request, uidb64, token):
    # validate the user using uid and token
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "please reset your password")
        return redirect(reverse("reset_password"))
    else:
        messages.warning(request, "this link has been expired")
        return redirect(reverse("login"))


class ResetPasswordView(FormView):
    template_name = "accounts/reset-password-page.html"
    form_class = ResetPasswordForm
    success_url = "/login/"

    def form_valid(self, form):
        pk = self.request.session.get("uid")
        user = User.objects.get(pk=pk)
        user.set_password(form.cleaned_data["password"])
        user.is_active = True
        user.save()
        messages.success(self.request, "Your password has been reset.")
        return super().form_valid(form)
