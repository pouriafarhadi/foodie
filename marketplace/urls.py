from django.urls import path

from marketplace import views

urlpatterns = [
    path("", views.MarketplaceView.as_view(), name="marketplace"),
    path(
        "<slug:slug>/", views.MarketplaceDetailView.as_view(), name="detail-marketplace"
    ),
]
