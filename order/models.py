import simplejson as json
from django.db import models
from accounts.context_processors import get_vendor
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor

request_object = ""


class Payment(models.Model):
    PAYMENT_METHOD = (
        ("PayPal", "PayPal"),
        ("zarinpal", "zarinpal"),  # for Iranians
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10, blank=True)
    total = models.FloatField()
    total_tax = models.FloatField()
    total_data = models.JSONField(null=True, blank=True)
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default="New")
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def order_placed_to(self):
        return ", ".join(str(i) for i in self.vendors.all())

    def get_total_by_vendor(self):
        vendor = get_vendor(request_object).get("vendor")
        if self.total_data:
            total_data = json.loads(self.total_data)
            subtotal = total_data.get(str(vendor.id)).get("subtotal")
            tax_amount = round((9 * subtotal) / 100, 2)
            grand_total = subtotal + tax_amount
            context = {
                "grand_total": grand_total,
                "subtotal": subtotal,
                "tax_amount": tax_amount,
            }
            return context
        return {"grand_total": 0, "subtotal": 0, "tax_amount": 0}

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_name
