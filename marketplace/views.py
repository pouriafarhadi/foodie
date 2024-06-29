from datetime import date

from django.db.models import Count, Prefetch, Q
from django.http import HttpResponse, JsonResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib import messages
from marketplace.context_processors import get_cart_counter, get_cart_amounts
from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor, OpeningHours


class MarketplaceView(ListView):

    template_name = "marketplace/listings.html"
    model = Vendor
    context_object_name = "vendors"
    paginate_by = 3
    ordering = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendors_count = self.get_queryset().count()
        context["vendors_count"] = vendors_count
        return context

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_approved=True, user__is_active=True)
        return query


class MarketplaceDetailView(TemplateView):
    template_name = "marketplace/single-marketplace-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = Vendor.objects.filter(
            is_approved=True, user__is_active=True, vendor_slug=kwargs["slug"]
        ).first()
        categories = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch("food_items", queryset=FoodItem.objects.filter(is_available=True))
        )
        opening_hours = OpeningHours.objects.filter(vendor=vendor).order_by(
            "day", "-from_hour"
        )
        today = date.today().isoweekday()
        current_opening_hours = OpeningHours.objects.filter(vendor=vendor, day=today)
        if self.request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=self.request.user)
        else:
            cart_items = None
        context["vendor"] = vendor
        context["categories"] = categories
        context["cart_items"] = cart_items
        context["opening_hours"] = opening_hours
        context["current_opening_hours"] = current_opening_hours
        return context


class AddToCart(View):
    def get(self, request: HttpRequest, food_id):
        if request.user.is_authenticated:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                # Check if the food item exists
                try:
                    fooditem = FoodItem.objects.get(id=food_id)
                    # Check if the user has already added that food item to the cart
                    try:
                        chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                        # Increase the Cart quantity
                        chkCart.quantity += 1
                        chkCart.save()
                        return JsonResponse(
                            {
                                "status": "success",
                                "message": "increased the food quantity!",
                                "cart_counter": get_cart_counter(request),
                                "qty": chkCart.quantity,
                                "cart_amount": get_cart_amounts(request),
                            }
                        )
                    except:
                        chkCart = Cart.objects.create(
                            user=request.user, fooditem=fooditem, quantity=1
                        )
                        return JsonResponse(
                            {
                                "status": "success",
                                "message": "Added the food to the Cart",
                                "cart_counter": get_cart_counter(request),
                                "qty": chkCart.quantity,
                                "cart_amount": get_cart_amounts(request),
                            }
                        )
                except:
                    return JsonResponse(
                        {"status": "Failed", "message": "This food does not exist"}
                    )
            else:
                return JsonResponse({"status": "Failed", "message": "Invalid request"})
        else:

            return JsonResponse(
                {"status": "login_required", "message": "Please login to continue"}
            )


class DecreaseCart(View):
    def get(self, request: HttpRequest, food_id):
        if request.user.is_authenticated:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                # Check if the food item exists
                try:
                    fooditem = FoodItem.objects.get(id=food_id)
                    # Check if the user has already added that food item to the cart
                    try:
                        chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                        # Decrease the Cart quantity
                        if chkCart.quantity > 1:
                            # Decrease the cart quantity
                            chkCart.quantity -= 1
                            chkCart.save()

                        else:
                            chkCart.delete()
                            chkCart.quantity = 0
                        return JsonResponse(
                            {
                                "status": "success",
                                "message": "Decreased the food quantity!",
                                "cart_counter": get_cart_counter(request),
                                "qty": chkCart.quantity,
                                "cart_amount": get_cart_amounts(request),
                            }
                        )
                    except:
                        return JsonResponse(
                            {
                                "status": "Failed",
                                "message": "you don't have any fooditem in your cart",
                            }
                        )
                except:
                    return JsonResponse(
                        {"status": "Failed", "message": "This food does not exist"}
                    )
            else:
                return JsonResponse({"status": "Failed", "message": "Invalid request"})
        else:
            return JsonResponse(
                {"status": "login_required", "message": "Please login to continue"}
            )


class CartView(TemplateView):
    template_name = "marketplace/cart-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_carts = Cart.objects.filter(user=user).order_by("created_at")
        context["carts"] = user_carts
        return context


class DeleteCart(View):
    def get(self, request: HttpRequest, cart_id):
        if request.user.is_authenticated:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                try:
                    # Check if the cart item exists
                    cart_item = Cart.objects.get(user=request.user, id=cart_id)
                    if cart_item:
                        cart_item.delete()
                        return JsonResponse(
                            {
                                "status": "Success",
                                "message": "Card deleted",
                                "cart_counter": get_cart_counter(request),
                                "cart_amount": get_cart_amounts(request),
                            }
                        )
                except:
                    return JsonResponse(
                        {"status": "Failed", "message": "This cart does not exist"}
                    )
            else:
                return JsonResponse({"status": "Failed", "message": "Invalid request"})
        else:
            return JsonResponse(
                {"status": "login_required", "message": "Please login to continue"}
            )


def search(request):
    restaurant_name = request.GET.get("res_name")
    food_name = request.GET.get("food_name")
    location = request.GET.get("location")
    if restaurant_name or food_name or location:
        fetch_vendors_by_fooditem = FoodItem.objects.filter(
            (
                Q(food_name__icontains=food_name)
                | Q(category__category_name__icontains=food_name)
            )
            & Q(is_available=True)
        ).values_list("vendor", flat=True)
        print(fetch_vendors_by_fooditem)
        vendors = Vendor.objects.filter(
            Q(id__in=fetch_vendors_by_fooditem)
            & Q(
                vendor_name__icontains=restaurant_name,
                is_approved=True,
                user__is_active=True,
            )
        )

        context = {"vendors": vendors, "vendors_count": vendors.count()}
        return render(request, "marketplace/listings.html", context)
    else:
        messages.info(request, "Please enter restaurant name or food name or location")
        return redirect("home-page")
