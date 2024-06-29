# Generated by Django 5.0.6 on 2024-06-29 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tax",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tax_type", models.CharField(max_length=50, unique=True)),
                (
                    "tax_percent",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        verbose_name="Tax Percentage (%)",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Tax",
                "verbose_name_plural": "Taxes",
            },
        ),
    ]
