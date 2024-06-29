from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages


class Cprofile(View):
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
        context = {"profile_form": profile_form, "user_form": user_form}
        return render(request, "customer/customer-profile-page.html", context)

    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("customer_profile")
        context = {"profile_form": profile_form, "user_form": user_form}
        return render(request, "customer/customer-profile-page.html", context)
