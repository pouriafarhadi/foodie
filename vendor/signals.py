from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Vendor


@receiver(post_save, sender=Vendor)
def post_save_vendor(sender, instance, created, **kwargs):
    if created:
        instance.vendor_slug = (
            slugify(instance.vendor_name) + f"-{str(instance.pk + 4545)}"
        )
        instance.save()
    else:
        return
