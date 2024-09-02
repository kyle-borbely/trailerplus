from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
    ObjectList,
    TabbedInterface,
    FieldRowPanel,
)
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail_meta_preview.panels import FacebookFieldPreviewPanel

from home.models import Partners, Footer, Header
from menus.models import MainMenu
from streams import blocks
from api.models import ServiceReviews
from product.models import CategoryMap

from trailersplus.utils.decorators import define_user_location, additional_context

class FlatPage(Page):
    template = "flatpage/flat_page.html"

    content = StreamField(
        [
            ("custom_trailer_form", blocks.CustomTrailerForms()),
            ("fleet_sales_forms", blocks.FleetSalesForms()),
            ("slider_block", blocks.SliderBlock()),
            ("big_text_section_block", blocks.BigTextSection()),
            ("category_carousel", blocks.CategoryCarousel()),
            ("call_to_action", blocks.CallToActionBlock()),
            ("call_to_action_v2", blocks.CallToActionV2()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ("partners", blocks.PartnersBlock()),
            ("big_banner", blocks.BigBanner()),
            ("big_banner_v2", blocks.BigBannerV2()),
            ("banner_search", blocks.BannerSearch()),
            ("banner_breadcrumbs", blocks.BannerBreadCrumbs()),
            ("banners_block", blocks.BannersLink()),
            ("youtube_banner", blocks.YoutubeBanner()),
            ("recent_works", blocks.RecentWorksBlock()),
            ("carousel_popup", blocks.CarouselPopup()),
            ("popular_parts_tabs", blocks.PartsAndAccessoriesBlock()),
            ("h2_title", blocks.H2Title()),
            ("h3_title", blocks.H3Title()),
            ("text_block", blocks.TextBlock()),
            ("text_background_image", blocks.TextAreaBackgroundImage()),
            ("richtext_block", blocks.RichtextBlock()),
            ("richtext_block_plus", blocks.RichtextBlockPlus()),
            ("return_policy_block", blocks.ReturnPolicy()),
            ("single_image_block", blocks.SingleImage()),
            ("image_and_text", blocks.ImageAndText()),
            ("image_gallery", blocks.ImageGallery()),
            ("image_gallery_v2", blocks.ImageGalleryV2()),
            ("image_carousel", blocks.ImagesCarousel()),
            ("buttons_block", blocks.ButtonsBlock()),
            ("image_icon_navigation_block", blocks.ImageIconNavigationBlock()),
            ("image_text_block", blocks.ImagesTextBlocks()),
            ("share_btn", blocks.ShareBtn()),
            ("trustpilot_widget", blocks.TrustPilotWidget()),
            ("call_us_block", blocks.CallUsBlock()),
            ("call_us_today", blocks.CallUsToday()),
            ("call_us_today_v2", blocks.CallUsTodayV2()),
            ("call_now_block", blocks.CallNowBlock()),
            ("youtube_block", blocks.YoutubeEmbedBlock()),
            ("why_buy_youtube", blocks.WhyBuyYoutube()),
            ("divider_line", blocks.DividerLine()),
            ("search_and_repair_banner", blocks.ServiceAndRepairBanner()),
            ("before_after_slider", blocks.BeforeAfterSlider()),
            ("table_row", blocks.TableRow()),
            ("store_finder_map", blocks.StoreFinderMap()),
            ("fleet_sales_banner", blocks.FleetSalesBanner()),
            ("why_choose_us", blocks.WhyChooseUs()),
            ("case_studies_carousel", blocks.CaseStudiesCarousel()),
            ("learn_more_block", blocks.LearnMoreBlock()),
            ("why_wait_block", blocks.WhyWaitBlock()),
            ("why_wait_block_v2", blocks.WhyWaitBlockV2()),
            ("models_offer_block", blocks.ModelsWeOfferBlock()),
            ("trailer_size_block", blocks.TrailersSizeBlock()),
            ("blockquotes_block", blocks.BlockquotesReview()),
            ("article_sidebar_block", blocks.ArticleSidebar()),
            ("service_icons_block", blocks.ServiceIconsBlock()),
            ("checkpoint_list_block", blocks.CheckpointList()),
            ("about_us_image_text_block", blocks.AboutUsImagesTextButton()),
            ("contact_us_block", blocks.ContactUsBlock()),
            ("financing_cards", blocks.FinancingCards()),
            ("options_block", blocks.OptionsBlock()),
            ("options_block_v2", blocks.OptionsBlockV2()),
            ("careers_block", blocks.VacanciesSection()),
            ("resources_block", blocks.ResourcesBlock()),
            ("trailer_we_offer_block", blocks.TrailersOfferImagesBlocks()),
            ("trailer_we_options_block", blocks.TrailersOfferOptionsLinks()),
            ("why_service_text_button", blocks.WhyServiceTextButton()),
            ("why_service_list_buttons", blocks.WhyServiceListButtons()),
            ("reviews_gallery", blocks.ReviewsGallery()),
        ],
        null=True,
        blank=True,
    )

    field_for_schema = models.TextField(blank=True, null=True)
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
        FieldPanel("field_for_schema"),
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
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["reviews"] = ServiceReviews.objects.all().order_by("-created_at")[:10]
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
        verbose_name = "Flat Page"
        verbose_name_plural = "Flat Pages"
