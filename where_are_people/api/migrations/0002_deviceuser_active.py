# Generated by Django 5.2.1 on 2025-05-23 17:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="deviceuser",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
