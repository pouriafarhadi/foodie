# Generated by Django 5.0.6 on 2024-06-09 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_alter_category_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fooditem",
            name="food_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="fooditem",
            name="slug",
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
