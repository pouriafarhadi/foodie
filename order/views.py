from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from marketplace.context_processors import get_cart_amounts
from marketplace.models import Cart
from .forms import OrderForm
from .models import Order, Payment, OrderedFood
from .utils import generate_order_number


@login_required(login_url="/login/")
def placeOrder(request):
    carts = Cart.objects.filter(user=request.user).order_by("created_at")
    cart_count = carts.count()
    if cart_count <= 0:
        return redirect("marketplace")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            """get prices"""
            reason = get_cart_amounts(request)
            subtotal = reason["subtotal"]
            grand_total = reason["grandtotal"]
            tax = reason["tax"]
            """create order"""
            order = Order(**form.cleaned_data)
            order.user = request.user
            order.total = grand_total
            order.total_tax = tax
            order.payment_method = request.POST["payment_method"]
            order.save()
            order.order_number = generate_order_number(order.id)
            """
            is_ordered should not set to be true until payment completed
             in this project we do not have real payment so i assume payment is successfully completed 
            """
            order.is_ordered = True
            order.save()
            """create payment object"""
            payment = Payment.objects.create(
                user=request.user,
                transaction_id="111111112223333",
                payment_method="zarinpal",
                amount=grand_total,
                status="successful",
            )
            """create ordered food"""
            cart_items = Cart.objects.filter(user=request.user)
            order.payment = payment
            order.save()
            for item in cart_items:
                ordered_food = OrderedFood.objects.create(
                    order=order,
                    payment=payment,
                    user=request.user,
                    fooditem=item.fooditem,
                    quantity=item.quantity,
                    price=item.fooditem.price,
                    amount=(item.fooditem.price * item.quantity),
                )
                item.delete()
            return redirect(
                reverse(
                    "order_complete",
                    kwargs={
                        "order_num": order.order_number,
                        "transaction_id": payment.transaction_id,
                        "waiting": "True",
                    },
                )
            )
        else:
            print(form.errors)
    return render(request, "order/place-order-page.html")


@login_required(login_url="/login/")
def orderComplete(request, order_num, transaction_id, waiting=None):
    if waiting == "True":
        message = "We can Assume that you have paid successfully"
        context = {
            "message": message,
            "order_num": order_num,
            "transaction_id": transaction_id,
        }
        return render(request, "order/paying-the-order-page.html", context)
    else:

        order = Order.objects.get(
            order_number=order_num,
            payment__transaction_id=transaction_id,
            is_ordered=True,
        )
        if order.user == request.user:
            ordered_food = OrderedFood.objects.filter(order=order)
            st = order.total - order.total_tax
            context = {
                "order": order,
                "ordered_food": ordered_food,
                "st": st,
            }
            return render(request, "order/order-complete-page.html", context)
        raise PermissionDenied
