from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import User, UserProfile
from .validators import allow_only_images_validator


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, validators=[validate_password]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error("password", e)

            if password != confirm_password:
                self.add_error("confirm_password", "Passwords must match")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords must match")
        return password


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(
        validators=[allow_only_images_validator],
        widget=forms.FileInput(attrs={"class": "btn btn-info", "accept": "image/*"}),
    )
    cover_photo = forms.FileField(
        validators=[allow_only_images_validator],
        widget=forms.FileInput(attrs={"class": "btn btn-info", "accept": "image/*"}),
    )

    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "cover_photo",
            "address",
            "country",
            "state",
            "city",
            "latitude",
            "longitude",
        ]

        widgets = {
            "address": forms.TextInput(
                attrs={"placeholder": "Start typing...", "required": "required"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "latitude" or field == "longitude":
                self.fields[field].widget.attrs.update({"readonly": "readonly"})

    def clean_latitude(self):
        if self.instance.latitude != self.cleaned_data.get("latitude"):
            self.add_error("latitude", "You may not change this field")
        return self.instance.latitude

    def clean_longitude(self):
        if self.instance.longitude != self.cleaned_data.get("longitude"):
            self.add_error("longitude", "You may not change this field")
        return self.instance.longitude


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number")
