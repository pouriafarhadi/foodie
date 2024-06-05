from django.contrib.auth.decorators import login_required
from django.urls import path

from vendor import views
from accounts import views as accounts_views

urlpatterns = [
    path("", login_required(accounts_views.VendorDashboard.as_view())),
    path("profile/", views.vprofile, name="vprofile"),
]
