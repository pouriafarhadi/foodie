from django.contrib.auth.decorators import login_required
from django.urls import path

from vendor import views
from accounts import views as accounts_views

urlpatterns = [
    path(
        "",
        login_required(accounts_views.VendorDashboard.as_view(), login_url="/login/"),
    ),
    path("profile/", views.vprofile, name="vprofile"),
    path(
        "opening_hours/",
        login_required(views.OpeningHourView.as_view(), login_url="/login/"),
        name="opening-hours",
    ),
    path(
        "opening_hours/add/",
        views.addingopeninghours,
        name="opening-hours-add",
    ),
    path(
        "opening_hours/remove/<int:pk>/",
        views.removeopeninghour,
        name="opening-hours-remove",
    ),
    path(
        "menu-builder/",
        login_required(views.MenuBuilderView.as_view(), login_url="/login/"),
        name="menu-builder",
    ),
    # Category CRUD
    path(
        "menu-builder/category/add/",
        login_required(views.AddCategory.as_view(), login_url="/login/"),
        name="add-category",
    ),
    path(
        "menu-builder/category/edit/<slug:slug>",
        login_required(views.EditCategory.as_view(), login_url="/login/"),
        name="edit-category",
    ),
    path(
        "menu-builder/category/delete/<slug:slug>",
        login_required(views.DeleteCategory.as_view(), login_url="/login/"),
        name="delete-category",
    ),
    path(
        "menu-builder/category/<slug:category_slug>/",
        login_required(views.FoodItemByCategory.as_view(), login_url="/login/"),
        name="food-item-by-category",
    ),
    # CRUD Food Item
    path(
        "menu-builder/food/add/",
        login_required(views.AddFoodItem.as_view(), login_url="/login/"),
        name="add-food-item",
    ),
    path(
        "menu-builder/food/edit/<slug:slug>/",
        login_required(views.EditFoodItem.as_view(), login_url="/login/"),
        name="edit-food-item",
    ),
    path(
        "menu-builder/food/delete/<slug:slug>/",
        login_required(views.DeleteFoodItem.as_view(), login_url="/login/"),
        name="delete-food-item",
    ),
    path(
        "my_orders/detail/<int:order_number>/<is_mine>",
        login_required(views.OrderDetailVendorView.as_view(), login_url="/login/"),
        name="order-detail-vendor",
    ),
    path(
        "my_orders/",
        login_required(views.MyOrdersVendorListView.as_view(), login_url="/login/"),
        name="my_orders_vendor",
    ),
]
