# Generated by Django 4.2.5 on 2023-11-12 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="id",
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
    ]