from django import forms

from vendor.models import Vendor


class RegisterRestaurantForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_license"]

        widgets = {"vendor_license": forms.FileInput(attrs={"class": "btn btn-info"})}
