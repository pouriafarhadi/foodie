from django.contrib.auth.decorators import login_required
from django.urls import path

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
        "custDashboard/", login_required(CustDashboard.as_view()), name="custDashboard"
    ),
    path(
        "vendorDashboard/",
        login_required(VendorDashboard.as_view()),
        name="vendorDashboard",
    ),
    path("myAccount/", login_required(myAccount.as_view()), name="myAccount"),
]
