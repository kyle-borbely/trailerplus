# Generated by Django 3.0.11 on 2021-04-05 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_auto_20200820_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='testinvoice',
            name='invoice_id',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Invoice ID'),
        ),
        migrations.AlterField(
            model_name='testinvoice',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]