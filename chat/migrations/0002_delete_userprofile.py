# Generated by Django 5.1.7 on 2025-03-15 06:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]
