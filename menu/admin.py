from django.contrib import admin

from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("category_name",)}
    pass


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("food_name",)}
    list_display = ("food_name", "price", "is_available")
