from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.views.generic import FormView, UpdateView
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.utils import checkIfItsVendor
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem
from .forms import RegisterRestaurantForm
from .models import Vendor
from .utils import get_vendor


@login_required(login_url="login")
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "GET":
        checkIfItsVendor(request)
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


class MenuBuilderView(View):
    def get(self, request):
        checkIfItsVendor(request)
        vendor = get_vendor(request)
        categories = Category.objects.filter(vendor=vendor)
        context = {"categories": categories}
        return render(request, "vendor/menu-builder-page.html", context)


class FoodItemByCategory(View):
    def get(self, request, category_slug):
        checkIfItsVendor(request)
        context = dict()
        try:
            vendor = get_vendor(request)
            foodItems = FoodItem.objects.filter(
                vendor=vendor, category__slug=category_slug
            )
            context = {
                "foodItems": foodItems,
                "category": foodItems.first().category,
                "food_exist": True,
            }
        except:
            messages.info(request, "no food items found! Add food item first")
            context["food_exist"] = False
        return render(request, "vendor/food-item-by-category-page.html", context)


class AddCategory(FormView):
    def get(self, request, *args, **kwargs):
        checkIfItsVendor(request)
        return super().get(request, *args, **kwargs)

    template_name = "vendor/add-category-page.html"
    form_class = CategoryForm

    def get_success_url(self):
        a = reverse("menu-builder")
        messages.success(self.request, "You have successfully added a new category!")
        return a

    def form_valid(self, form):
        a = form.save(commit=False)
        a.vendor = get_vendor(self.request)
        try:
            a.save()
        except IntegrityError:
            messages.warning(self.request, "You have already added this category!")
            return redirect("add-category")
        return super().form_valid(form)


class EditCategory(View):
    def get(self, request, slug):
        checkIfItsVendor(request)
        vendor = get_vendor(request)
        category = get_object_or_404(Category, slug=slug, vendor=vendor)
        form = CategoryForm(instance=category)
        context = {
            "form": form,
            "category": category,
        }
        return render(request, "vendor/edit-category-page.html", context)

    def post(self, request, slug):
        vendor = get_vendor(request)
        category = get_object_or_404(Category, slug=slug, vendor=vendor)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully edited this category!")
            return redirect("menu-builder")
        context = {
            "form": form,
            "category": category,
        }
        return render(request, "vendor/edit-category-page.html", context)


class DeleteCategory(View):
    def get(self, request, slug):

        checkIfItsVendor(request)
        vendor = get_vendor(request)
        category = get_object_or_404(Category, slug=slug, vendor=vendor)
        name = category.category_name
        category.delete()
        messages.success(request, f"You have successfully deleted {name} category!")
        return redirect("menu-builder")


class AddFoodItem(FormView):
    category_slug_for_url = None
    template_name = "vendor/add-food-item-page.html"
    form_class = FoodItemForm

    def get(self, request, *args, **kwargs):
        checkIfItsVendor(request)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        a = reverse("food-item-by-category", args=[self.category_slug_for_url])
        messages.success(self.request, "You have successfully added a new food!")
        return a

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        vendor = get_vendor(self.request)
        return form_class(vendor=vendor, **self.get_form_kwargs())

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.vendor = get_vendor(self.request)
        try:
            obj.save()
            self.category_slug_for_url = obj.category.slug
        except IntegrityError:
            messages.warning(self.request, "You have already added this food!")
            return redirect("add-food-item")
        return super().form_valid(form)


class EditFoodItem(View):
    def get(self, request, slug):
        checkIfItsVendor(request)
        vendor = get_vendor(request)
        food = get_object_or_404(FoodItem, slug=slug, vendor=vendor)
        form = FoodItemForm(vendor=vendor, instance=food)
        context = {
            "form": form,
            "food": food,
        }
        return render(request, "vendor/edit-food-item-page.html", context)

    def post(self, request, slug):
        vendor = get_vendor(request)
        food = get_object_or_404(FoodItem, slug=slug, vendor=vendor)
        form = FoodItemForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully edited this food!")
            return redirect(reverse("food-item-by-category", args=[food.category.slug]))
        context = {
            "form": form,
            "food": food,
        }
        return render(request, "vendor/edit-food-item-page.html", context)


class DeleteFoodItem(View):
    def get(self, request, slug):
        checkIfItsVendor(request)
        vendor = get_vendor(request)
        food = get_object_or_404(FoodItem, slug=slug, vendor=vendor)
        name = food.food_name
        slug = food.category.slug
        food.delete()
        messages.success(request, f"You have successfully deleted {name} food!")
        return redirect(reverse("food-item-by-category", args=[slug]))
