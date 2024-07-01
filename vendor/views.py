from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpRequest, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.views.generic import FormView, UpdateView, TemplateView, ListView
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.utils import checkIfItsVendor
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem
from order.models import Order, OrderedFood
from .forms import RegisterRestaurantForm, OpeningHoursForm
from .models import Vendor, OpeningHours
from .utils import get_vendor
from django.db.models import Case, When, BooleanField


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


class OpeningHourView(View):

    def get(self, request):
        checkIfItsVendor(request)
        vendor = get_vendor(request)
        opening_hours = OpeningHours.objects.filter(vendor=vendor)
        form = OpeningHoursForm()
        context = {"form": form, "opening_hours": opening_hours}
        return render(request, "vendor/opening-hours-page.html", context)


@login_required(login_url="login")
def addingopeninghours(request):
    if request.user.is_authenticated:
        checkIfItsVendor(request)
        if (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            and request.method == "POST"
        ):
            vendor = get_vendor(request)
            res = request.POST
            try:
                hour = OpeningHours.objects.create(
                    vendor=vendor,
                    day=res.get("day"),
                    from_hour=res.get("from_hour"),
                    to_hour=res.get("to_hour"),
                    is_closed=res.get("is_closed"),
                )
                if hour:
                    day = OpeningHours.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {
                            "status": "success",
                            "id": hour.id,
                            "daay": day.get_day_display(),
                            "is_closed": "Closed",
                        }
                    else:
                        response = {
                            "status": "success",
                            "id": hour.id,
                            "daay": day.get_day_display(),
                            "from_hour": day.from_hour,
                            "to_hour": day.to_hour,
                        }
            except IntegrityError as e:
                response = {
                    "status": "failed",
                    "message": f"the time you choose already exists",
                }
            return JsonResponse(response)
        else:
            raise Http404
    else:
        return Http404


def removeopeninghour(request, pk):
    if request.user.is_authenticated:
        checkIfItsVendor(request)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            hour = get_object_or_404(OpeningHours, id=pk)
            hour.delete()
            return JsonResponse({"status": "success", "id": pk})
        else:
            raise Http404
    else:
        return Http404


class OrderDetailVendorView(View):
    def get(self, request, order_number, is_mine):
        checkIfItsVendor(request)
        order = get_object_or_404(Order, order_number=order_number)
        print(is_mine)
        if is_mine == "vendor":
            ordered_food = OrderedFood.objects.filter(
                order=order, fooditem__vendor=get_vendor(request)
            )
            order_data = order.get_total_by_vendor()
            context = {
                "order": order,
                "ordered_food": ordered_food,
                "subtotal": order_data.get("subtotal"),
                "tax": order_data.get("tax_amount"),
                "grand_total": order_data.get("grand_total"),
            }
            return render(request, "vendor/order-detail-vendor-page.html", context)
        elif is_mine == "cust":
            ordered_food = OrderedFood.objects.filter(order=order)
            subtotal = 0
            for item in ordered_food:
                subtotal += item.quantity * item.price

            if order.user != request.user:
                raise PermissionDenied
            if not order.is_ordered:
                raise Http404
            context = {
                "order": order,
                "ordered_food": ordered_food,
                "subtotal": subtotal,
                "tax": order.total_tax,
                "grand_total": order.total,
            }
            return render(request, "vendor/order-detail-vendor-page.html", context)


"""
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
"""


class MyOrdersVendorListView(ListView):
    template_name = "vendor/vendor-orders-list-page.html"
    model = Order
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        query = super().get_queryset().filter(user=self.request.user, is_ordered=True)
        vendor = get_vendor(self.request)

        # Combine the two queries
        vendor_orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True)
        # Combine both querysets and ensure unique results
        combined_query = query | vendor_orders
        combined_query = combined_query.annotate(
            mine=Case(
                When(vendors__in=[vendor.id], then=True),
                default=False,
                output_field=BooleanField(),
            )
        ).order_by("-created_at")

        return combined_query
