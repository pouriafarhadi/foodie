from .models import Cart
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = 0
    tax = 9
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            price = item.fooditem.price
            subtotal += price * item.quantity
        tax_amount = round((tax * subtotal) / 100, 2)
        tax_name = "Value-added tax (VAT)"
        grand_total = subtotal + tax_amount
    else:
        tax_amount = 0
    return dict(subtotal=subtotal, tax=tax_amount, grandtotal=grand_total)
