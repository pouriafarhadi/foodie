from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from vendor.models import Vendor


class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category_name"]
        verbose_name = "category"
        verbose_name_plural = "categories"
        unique_together = (("vendor", "category_name"),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor.vendor_name}-{self.category_name}"


class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="food_items"
    )
    food_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.ImageField(upload_to="food_images/", blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["food_name"]
        verbose_name = "food item"
        verbose_name_plural = "food items"
        unique_together = (("vendor", "category", "food_name"),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.food_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.food_name
