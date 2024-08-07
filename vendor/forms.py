from django import forms

from vendor.models import Vendor, OpeningHours
from accounts.validators import allow_only_images_validator


class RegisterRestaurantForm(forms.ModelForm):
    vendor_license = forms.FileField(
        validators=[allow_only_images_validator],
        widget=forms.FileInput(attrs={"class": "btn btn-info", "accept": "image/*"}),
    )

    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_license"]


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ["day", "from_hour", "to_hour", "is_closed"]
