# Generated by Django 3.0.9 on 2020-08-12 15:25

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='cookie_popup',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='footer',
            name='cookie_popup_en',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='footer',
            name='cookie_popup_es',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
