import os

from django.core.exceptions import ValidationError


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    if ext.lower() not in ["jpg", "jpeg", "png", ".jpg", ".jpeg", ".png"]:
        raise ValidationError("Only jpg, jpeg and png files are allowed")
