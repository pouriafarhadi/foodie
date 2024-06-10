from django import forms

from accounts.validators import allow_only_images_validator
from menu.models import Category, FoodItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(
        required=False,
        validators=[allow_only_images_validator],
        widget=forms.FileInput(attrs={"class": "btn btn-info", "accept": "image/*"}),
    )

    class Meta:
        model = FoodItem
        fields = [
            "food_name",
            "category",
            "description",
            "price",
            "image",
            "is_available",
        ]

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop("vendor", None)
        super(FoodItemForm, self).__init__(*args, **kwargs)
        if vendor:
            self.fields["category"].queryset = Category.objects.filter(vendor=vendor)
            self.fields["category"].label_from_instance = lambda obj: obj.category_name
