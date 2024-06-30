from django.contrib import admin
from .models import Order, Payment, OrderedFood


class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = (
        "order",
        "payment",
        "user",
        "fooditem",
        "quantity",
        "price",
        "amount",
    )
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "total")
    inlines = [OrderedFoodInline]


admin.site.register(Payment)
admin.site.register(OrderedFood)
