# Generated by Django 3.2.19 on 2023-07-09 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_auto_20230709_1941'),
        ('journal', '0003_auto_20230709_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scielojournal',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='collection.collection'),
        ),
    ]
