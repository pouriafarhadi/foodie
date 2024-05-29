from django.urls import path

from accounts import views
from accounts.views import UserRegistrationView

urlpatterns = [
    path("registerUser/", UserRegistrationView.as_view(), name="registerUser"),
]
