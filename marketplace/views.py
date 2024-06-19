from django.db.models import Count, Prefetch
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View

from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor


class MarketplaceView(ListView):
    template_name = "marketplace/listings.html"
    model = Vendor
    context_object_name = "vendors"
    paginate_by = 1
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
        context["vendor"] = vendor
        context["categories"] = categories
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
                {"status": "Failed", "message": "Please login to continue"}
            )
