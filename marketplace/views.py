from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from menu.models import Category, FoodItem
from vendor.models import Vendor


class MarketplaceView(ListView):
    template_name = "marketplace/listings.html"
    model = Vendor
    context_object_name = "vendors"
    paginate_by = 1

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
