from django.db import models
from django.utils.text import slugify

from accounts.models import User, UserProfile
from accounts.utils import send_notification


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="userprofile"
    )
    vendor_name = models.CharField(max_length=100)
    vendor_slug = models.SlugField(max_length=200, unique=True, blank=True)
    vendor_license = models.ImageField(upload_to="vendor/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.pk is not None:
            # update user
            original = Vendor.objects.get(pk=self.pk)
            if original.is_approved != self.is_approved:
                mail_template = "vendor/emails/admin-approval-email.html"
                context = {"user": self.user, "is_approved": self.is_approved}
                if self.is_approved:
                    # send notification email
                    mail_subject = "Congratulations, your restaurant has been approved"
                    send_notification(mail_subject, mail_template, context)
                else:
                    # send notification email
                    mail_subject = "We're sorry, you are not eligible for publishing your food menu on our marketplace !"
                    send_notification(mail_subject, mail_template, context)
        if not self.vendor_slug:
            self.vendor_slug = slugify(self.vendor_name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.vendor_name
