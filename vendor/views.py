from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.utils import detectUser
from .forms import RegisterRestaurantForm
from .models import Vendor


@login_required(login_url="login")
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "GET":
        if detectUser(request.user) != "vendorDashboard":
            raise PermissionDenied
        profile_form = UserProfileForm(instance=profile)
        vendor_form = RegisterRestaurantForm(instance=vendor)

    elif request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = RegisterRestaurantForm(
            request.POST, request.FILES, instance=vendor
        )
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("vprofile")

    return render(
        request,
        "vendor/vprofile-page.html",
        context={"profile_form": profile_form, "vendor_form": vendor_form},
    )
