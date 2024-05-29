from django.urls import path

from accounts import views
from accounts.views import UserRegistrationView, RestaurantRegistrationView

urlpatterns = [
    path("registerUser/", UserRegistrationView.as_view(), name="registerUser"),
    path(
        "registerRestaurant/",
        RestaurantRegistrationView.as_view(),
        name="registerRestaurant",
    ),
]
