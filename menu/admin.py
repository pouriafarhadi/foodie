from django.contrib import admin

from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("food_name", "price", "is_available")
