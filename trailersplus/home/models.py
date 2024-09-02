from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail_meta_preview.panels import FacebookFieldPreviewPanel

from menus.models import MainMenu
from streams import blocks

from api.models import ServiceReviews

from trailersplus.utils.decorators import define_user_location, additional_context

from product.models import CategoryMap


@register_snippet
class SearchBar(models.Model):
    trailer_type_text = models.CharField(max_length=255, blank=True, null=True)
    select_store_text = models.CharField(max_length=255, blank=True, null=True)
    search_button_text = models.CharField(max_length=255, blank=True, null=True)

    panels = [
        FieldPanel("trailer_type_text"),
        FieldPanel("select_store_text"),
        FieldPanel("search_button_text"),
    ]

    class Meta:
        verbose_name = "Search Bar"
        verbose_name_plural = "Search Bars"


@register_snippet
class Header(models.Model):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    svg_logo = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+"
    )
    location_icon_text = models.TextField(null=True, blank=True)
    location_icon_mobile_text = models.TextField(null=True, blank=True)
    go_to_google_maps = models.CharField(max_length=25, blank=True)
    phone_icon_text = models.TextField(null=True, blank=True)
    cart_title = models.CharField(max_length=15, blank=True)
    item_added_text = models.CharField(max_length=30, blank=True)
    remove_button = models.CharField(max_length=15, blank=True)
    checkout_button = models.CharField(max_length=15, blank=True)

    panels = [
        ImageChooserPanel("logo"),
        DocumentChooserPanel("svg_logo"),
        FieldPanel("location_icon_text"),
        FieldPanel("location_icon_mobile_text"),
        FieldPanel("go_to_google_maps"),
        FieldPanel("phone_icon_text"),
        FieldPanel("cart_title"),
        FieldPanel("item_added_text"),
        FieldPanel("remove_button"),
        FieldPanel("checkout_button"),
    ]

    class Meta:
        verbose_name = "Header"
        verbose_name_plural = "Headers"


@register_snippet
class Footer(models.Model):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    svg_logo = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+"
    )
    top_text = models.CharField(max_length=300, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    visa_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    mastercard_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    american_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    discover_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    bottom_text = models.CharField(max_length=2000, null=True, blank=True)
    cookie_popup = RichTextField(blank=True, null=True)
    cookie_popup_button_text = models.CharField(max_length=255, blank=True, null=True)
    copyright_text = models.CharField(max_length=200, null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel("logo"),
                DocumentChooserPanel("svg_logo"),
                FieldPanel("top_text"),
                FieldPanel("location"),
                FieldPanel("phone_number"),
            ],
            heading="Footer Information",
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel("visa_image"),
                ImageChooserPanel("mastercard_image"),
                ImageChooserPanel("american_image"),
                ImageChooserPanel("discover_image"),
            ],
            heading="Payments Images",
        ),
        MultiFieldPanel(
            [
                FieldPanel("cookie_popup"),
                FieldPanel("cookie_popup_button_text")
            ]
        ),
        MultiFieldPanel(
            [FieldPanel("bottom_text"), FieldPanel("copyright_text")],
            heading="Copyright",
        ),
    ]

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"


@register_snippet
class Partners(Orderable, models.Model):
    partner_title = models.CharField(max_length=100)
    partner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    partner_image_alt = models.CharField(max_length=255, blank=True, null=True)
    partner_link = models.CharField(max_length=999, blank=True, null=True, help_text='https:// required!')

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("partner_title"),
                ImageChooserPanel("partner_image"),
                FieldPanel("partner_image_alt"),
                FieldPanel("partner_link"),
            ],
            heading="Partners",
        )
    ]

    def __str__(self):
        return self.partner_title

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"


class HomePage(Page):
    template = "home/home_page.html"

    content = StreamField(
        [
            ("slider_block", blocks.SliderBlock()),
            ("big_text_section_block", blocks.BigTextSection()),
            ("category_carousel", blocks.CategoryCarousel()),
            ("call_to_action", blocks.CallToActionBlock()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ("partners", blocks.PartnersBlock()),
            ("banners_block", blocks.BannersLink()),
            ("recent_works", blocks.RecentWorksBlock()),
            ("trustpilot_widget", blocks.TrustPilotWidget()),
            ("trustpilot_widget_horizontal", blocks.TrustPilotWidgetHorizontal()),
        ],
        null=True,
        blank=True,
    )

    og_title = models.CharField(max_length=500, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Og image",
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
        FacebookFieldPreviewPanel([
            FieldPanel("og_title"),
            FieldPanel("og_description"),
            ImageChooserPanel("og_image"),
        ], heading="Facebook")
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["search_bars"] = SearchBar.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["reviews"] = ServiceReviews.objects.all()[:10]
        context["categories"] = CategoryMap.objects.all()

        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    # @define_user_location
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


class ErrorPage(Page):
    template = "home/home_page.html"

    content = StreamField(
        [
            ("error_banner_block", blocks.ErrorBannerBlock()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ("partners", blocks.PartnersBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super(ErrorPage, self).get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()

        return context

    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    class Meta:
        verbose_name = "Error Page"
        verbose_name_plural = "Error Pages"
