# Generated by Django 4.2.5 on 2023-11-12 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_alter_item_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="register_date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="item",
            name="rental_date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="item",
            name="return_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
