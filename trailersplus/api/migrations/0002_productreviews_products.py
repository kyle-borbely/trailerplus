# Generated by Django 3.0.9 on 2020-08-06 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreviews',
            name='products',
            field=models.ManyToManyField(related_name='reviews', to='product.Trailer'),
        ),
    ]