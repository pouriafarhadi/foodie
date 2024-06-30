from django.urls import path
from django.contrib.auth.decorators import login_required
from accounts.views import CustDashboard
from .views import Cprofile, MyOrdersListView, MyOrderDetailView

urlpatterns = [
    path("", login_required(CustDashboard.as_view(), login_url="/login/")),
    path(
        "profile/",
        login_required(Cprofile.as_view(), login_url="/login/"),
        name="customer_profile",
    ),
    path(
        "my_orders/",
        login_required(MyOrdersListView.as_view(), login_url="/login/"),
        name="my_orders_list",
    ),
    path(
        "my_orders_detail/<int:order_number>/",
        login_required(MyOrderDetailView.as_view(), login_url="/login/"),
        name="my_order_detail",
    ),
]
