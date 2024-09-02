from django.db import models
from django.shortcuts import render
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel

from api.models import ServiceReviews
from home.models import Header, SearchBar, Partners, Footer
from menus.models import MainMenu
from streams import blocks


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(blank=True, null=True, help_text="Facebook link")
    instagram = models.URLField(blank=True, null=True, help_text="Instagram link")
    youtube = models.URLField(blank=True, null=True, help_text="Youtube link")

    panels = [
        MultiFieldPanel(
            [FieldPanel("facebook"), FieldPanel("instagram"), FieldPanel("youtube"),],
            heading="Social Media Settings",
        )
    ]


@register_setting
class ErrorPage404(BaseSetting):
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    background_image_mobile = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    sub_title = models.CharField(max_length=999, blank=True, null=True)
    textarea = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel("background_image"),
                ImageChooserPanel("background_image_mobile"),
            ], heading='Background Image'
        ),
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("sub_title"),
                FieldPanel("textarea"),
            ], heading='Text Section'
        ),
        MultiFieldPanel(
            [
                FieldPanel("button_text"),
                PageChooserPanel("button_page"),
            ], heading='Button Section'
        )
    ]


@register_setting
class AdditionalHtml(BaseSetting):
    head_code = models.TextField(blank=True, null=False, default='')
    body_code = models.TextField(blank=True, null=False, default='')

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('head_code'),
                FieldPanel('body_code'),
            ], heading="HTML code"
        )
    ]
