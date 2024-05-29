# Generated by Django 5.0.6 on 2024-05-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, "Restaurant"), (2, "Customer")],
                default=2,
                null=True,
            ),
        ),
    ]