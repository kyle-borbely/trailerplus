from django.db import models
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel


class Category(models.Model):
    title = models.CharField("Title", max_length=25, null=False)
    basetype = models.CharField("Base Type", max_length=255, null=False)
    description = RichTextField()
    category_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    # slug = models.SlugField()

    panels = [
        FieldPanel("title"),
        FieldPanel("basetype"),
        FieldPanel("description"),
        ImageChooserPanel("category_image"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
