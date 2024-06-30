from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView

from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages

from accounts.utils import checkIfItsCustomer
from order.models import Order, OrderedFood


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


class MyOrdersListView(ListView):
    template_name = "customer/my-orders-page.html"
    model = Order
    context_object_name = "orders"
    paginate_by = 2

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user=self.request.user, is_ordered=True).order_by(
            "-created_at"
        )
        return query


class MyOrderDetailView(View):
    def get(self, request, order_number):
        checkIfItsCustomer(request)
        order = get_object_or_404(Order, order_number=order_number)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += item.quantity * item.price

        if order.user != request.user:
            raise PermissionDenied
        if not order.is_ordered:
            raise Http404
        context = {"order": order, "ordered_food": ordered_food, "st": subtotal}
        return render(request, "customer/my-order-detail-page.html", context)
