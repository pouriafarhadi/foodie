# Generated by Django 5.0.6 on 2024-06-27 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0005_alter_openinghours_from_hour_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="openinghours",
            options={"ordering": ("day", "-from_hour")},
        ),
        migrations.AlterUniqueTogether(
            name="openinghours",
            unique_together={("vendor", "day", "from_hour", "to_hour")},
        ),
    ]
