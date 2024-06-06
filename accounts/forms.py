from django import forms

from accounts.models import User, UserProfile


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password")

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords must match")
        return password


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
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "cover_photo",
            "address_line_1",
            "address_line_2",
            "country",
            "state",
            "city",
            "pincode",
            "latitude",
            "longitude",
        ]

        widgets = {
            "profile_picture": forms.FileInput(attrs={"class": "btn btn-info"}),
            "cover_photo": forms.FileInput(attrs={"class": "btn btn-info"}),
        }
