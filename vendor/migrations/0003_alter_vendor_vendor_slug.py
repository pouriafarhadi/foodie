# Generated by Django 5.0.6 on 2024-06-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0002_vendor_vendor_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="vendor_slug",
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
