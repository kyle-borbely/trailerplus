# Generated by Django 3.0.9 on 2020-09-08 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_trailer_coupler'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='store_description_directions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='store_spanish_description_directions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
