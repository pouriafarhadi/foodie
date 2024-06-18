from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class MarketplaceView(TemplateView):
    template_name = "marketplace/listings.html"
