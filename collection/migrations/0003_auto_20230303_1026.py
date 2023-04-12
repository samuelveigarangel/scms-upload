# Generated by Django 3.2.12 on 2023-03-03 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='acron',
            field=models.TextField(blank=True, null=True, verbose_name='Collection Acronym'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.TextField(blank=True, null=True, verbose_name='Collection Name'),
        ),
        migrations.AlterField(
            model_name='scielofile',
            name='file_id',
            field=models.TextField(blank=True, null=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='scielofile',
            name='name',
            field=models.TextField(verbose_name='Filename'),
        ),
        migrations.AlterField(
            model_name='scielofile',
            name='object_name',
            field=models.TextField(blank=True, null=True, verbose_name='Object name'),
        ),
        migrations.AlterField(
            model_name='scielofile',
            name='relative_path',
            field=models.TextField(blank=True, null=True, verbose_name='Relative Path'),
        ),
        migrations.AlterField(
            model_name='scielojournal',
            name='title',
            field=models.TextField(blank=True, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='xmlfile',
            name='public_object_name',
            field=models.TextField(blank=True, null=True, verbose_name='Public object name'),
        ),
    ]