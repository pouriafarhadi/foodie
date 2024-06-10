from django.contrib.auth.decorators import login_required
from django.urls import path

from vendor import views
from accounts import views as accounts_views

urlpatterns = [
    path("", login_required(accounts_views.VendorDashboard.as_view())),
    path("profile/", views.vprofile, name="vprofile"),
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
]
