from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import placeOrder, orderComplete

urlpatterns = [
    path("place_order/", placeOrder, name="place_order"),
    path(
        r"^order_complete/(?P<order_num>\d+)/(?P<transaction_id>\w+)/(?P<waiting>(True|False))?$",
        orderComplete,
        name="order_complete",
    ),
]
