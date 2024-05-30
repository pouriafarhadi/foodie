from django.urls import path

from accounts import views
from accounts.views import (
    UserRegistrationView,
    RestaurantRegistrationView,
    LoginView,
    LogoutView,
    DashboardView,
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
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),
]
