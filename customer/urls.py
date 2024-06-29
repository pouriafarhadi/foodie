from django.urls import path
from django.contrib.auth.decorators import login_required
from accounts.views import CustDashboard
from .views import Cprofile

urlpatterns = [
    path("", login_required(CustDashboard.as_view(), login_url="/login/")),
    path(
        "profile/",
        login_required(Cprofile.as_view(), login_url="/login/"),
        name="customer_profile",
    ),
]
