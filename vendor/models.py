from datetime import time, date, datetime

from django.core.validators import MinValueValidator, MaxValueValidator
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
    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

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

    def is_open(self):
        today = date.today().isoweekday()
        current_opening_hours = OpeningHours.objects.filter(vendor=self, day=today)
        now = datetime.now()
        is_open = False
        for i in current_opening_hours:
            from_hour = i.from_hour
            to_hour = i.to_hour
            if from_hour and to_hour:
                try:
                    start = datetime.strptime(from_hour, "%I:%M %p").time()
                    end = datetime.strptime(to_hour, "%I:%M %p").time()
                    if start <= now.time() <= end:
                        is_open = True
                        break
                except ValueError as e:
                    continue
        return is_open

    def __str__(self):
        return self.vendor_name


DAYS = [
    (1, "monday"),
    (2, "tuesday"),
    (3, "wednesday"),
    (4, "thursday"),
    (5, "friday"),
    (6, "saturday"),
    (7, "sunday"),
]

HOURS_OF_DAY_24 = [
    (time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p"))
    for h in range(0, 24)
    for m in [0, 30]
]


class OpeningHours(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="opening_hours"
    )
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOURS_OF_DAY_24, max_length=20, blank=True)
    to_hour = models.CharField(choices=HOURS_OF_DAY_24, max_length=20, blank=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.get_day_display()

    class Meta:
        ordering = ("day", "-from_hour")
        unique_together = ("vendor", "day", "from_hour", "to_hour")
