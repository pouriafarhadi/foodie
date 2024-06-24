from django.urls import path
from django.contrib.auth.decorators import login_required
from marketplace import views

urlpatterns = [
    path("", views.MarketplaceView.as_view(), name="marketplace"),
    path(
        "cart/",
        login_required(views.CartView.as_view(), login_url="/login/"),
        name="cart",
    ),
    path(
        "<slug:slug>/", views.MarketplaceDetailView.as_view(), name="detail-marketplace"
    ),
    path("add_to_cart/<int:food_id>/", views.AddToCart.as_view(), name="add-to-cart"),
    path(
        "decrease_cart/<int:food_id>/",
        views.DecreaseCart.as_view(),
        name="decrease_cart",
    ),
    path("delete_cart/<int:cart_id>/", views.DeleteCart.as_view(), name="delete-cart"),
]
