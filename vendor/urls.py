from django.contrib.auth.decorators import login_required
from django.urls import path

from vendor import views
from accounts import views as accounts_views

urlpatterns = [
    path("", login_required(accounts_views.VendorDashboard.as_view())),
    path("profile/", views.vprofile, name="vprofile"),
    path(
        "opening_hours/",
        login_required(views.OpeningHourView.as_view()),
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
        login_required(views.MenuBuilderView.as_view()),
        name="menu-builder",
    ),
    # Category CRUD
    path(
        "menu-builder/category/add/",
        login_required(views.AddCategory.as_view()),
        name="add-category",
    ),
    path(
        "menu-builder/category/edit/<slug:slug>",
        login_required(views.EditCategory.as_view()),
        name="edit-category",
    ),
    path(
        "menu-builder/category/delete/<slug:slug>",
        login_required(views.DeleteCategory.as_view()),
        name="delete-category",
    ),
    path(
        "menu-builder/category/<slug:category_slug>/",
        login_required(views.FoodItemByCategory.as_view()),
        name="food-item-by-category",
    ),
    # CRUD Food Item
    path(
        "menu-builder/food/add/",
        login_required(views.AddFoodItem.as_view()),
        name="add-food-item",
    ),
    path(
        "menu-builder/food/edit/<slug:slug>/",
        login_required(views.EditFoodItem.as_view()),
        name="edit-food-item",
    ),
    path(
        "menu-builder/food/delete/<slug:slug>/",
        login_required(views.DeleteFoodItem.as_view()),
        name="delete-food-item",
    ),
]
