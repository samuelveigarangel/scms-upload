# Generated by Django 4.2.6 on 2024-04-01 02:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="pressrelease",
            unique_together={("url",)},
        ),
    ]