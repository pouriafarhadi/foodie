from django.contrib import admin

from vendor.models import Vendor, OpeningHours


class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor_name", "is_approved", "rating", "created_at")
    list_display_links = ("user", "vendor_name")
    list_editable = ("is_approved", "rating")


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ("vendor", "day", "from_hour", "to_hour")


admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHours, OpeningHoursAdmin)
