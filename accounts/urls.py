from django.contrib.auth.decorators import login_required
from django.urls import path, include

from accounts import views
from accounts.views import (
    UserRegistrationView,
    RestaurantRegistrationView,
    LoginView,
    LogoutView,
    myAccount,
    CustDashboard,
    VendorDashboard,
)


urlpatterns = [
    path("", login_required(myAccount.as_view(), login_url="/login/"), name="account"),
    path(
        "registerUser/",
        UserRegistrationView.as_view(),
        name="registerUser",
    ),
    path(
        "registerRestaurant/",
        RestaurantRegistrationView.as_view(),
        name="registerRestaurant",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "custDashboard/",
        login_required(CustDashboard.as_view(), login_url="/login/"),
        name="custDashboard",
    ),
    path(
        "vendorDashboard/",
        login_required(VendorDashboard.as_view(), login_url="/login/"),
        name="vendorDashboard",
    ),
    path(
        "myAccount/",
        login_required(myAccount.as_view(), login_url="/login/"),
        name="my-Account",
    ),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgotPassword/", views.forgot_password, name="forgotPassword"),
    path(
        "resetPasswordValidate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    path("resetPassword/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("vendor/", include("vendor.urls")),
    path("customer/", include("customer.urls")),
]
