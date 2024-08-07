"""
URL configuration for foodie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from foodie import views
from marketplace import views as MarketplaceViews
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomeView.as_view(), name="home-page"),
    path("", include("accounts.urls")),
    path("marketplace/", include("marketplace.urls")),
    path("search/", MarketplaceViews.search, name="search"),
    path(
        "checkout/",
        login_required(MarketplaceViews.Checkout.as_view(), login_url="/login/"),
        name="checkout",
    ),
    path("orders/", include("order.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
