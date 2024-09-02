from wagtail.admin.edit_handlers import FieldRowPanel
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class Menu(blocks.StructBlock):
    menus = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("menu_title", blocks.CharBlock()),
                ("menu_page", blocks.PageChooserBlock(required=False)),
                ("menu_items", blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("title", blocks.CharBlock(required=False)),
                            ("image", ImageChooserBlock(required=False)),
                            ("special_class", blocks.BooleanBlock(required=False, default=False, help_text='Special Class for PNG Image')),
                            ("link_url", blocks.CharBlock(required=False)),
                            ("link_page", blocks.PageChooserBlock(required=False)),
                        ]
                    )
                ),
                 ),
            ]
        ),
    )
    close_menu_button_text = blocks.CharBlock(max_length=30, required=False)

    class Meta:
        template = "streams/menus/main_menu.html"
        icon = "list-ul"
        label = "Menu"


class FleetSalesForms(blocks.StructBlock):
    section_description = blocks.TextBlock(required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)
    placeholder_name = blocks.CharBlock(max_length=255, required=False)
    placeholder_email = blocks.CharBlock(max_length=255, required=False)
    placeholder_phone = blocks.CharBlock(max_length=255, required=False)
    placeholder_fleet_size = blocks.CharBlock(max_length=255, required=False)
    placeholder_description = blocks.CharBlock(max_length=255, required=False)
    success_message = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "forms/fleet_sales_form.html"
        icon = "snippet"
        label = "Fleet Sales Forms"


class CustomTrailerForms(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)
    placeholder_name = blocks.CharBlock(max_length=255, required=False)
    placeholder_email = blocks.CharBlock(max_length=255, required=False)
    placeholder_zipcode = blocks.CharBlock(max_length=255, required=False)
    placeholder_description = blocks.CharBlock(max_length=255, required=False)
    success_message = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "forms/custom_trailer_form.html"
        icon = "snippet"
        label = "Custom Trailer Forms"


class SliderBlock(blocks.StructBlock):
    slides = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=False)),
                ("image_mobile", ImageChooserBlock(required=False)),
                ("image_alt", blocks.CharBlock(max_length=255, required=False)),
                (
                    "text",
                    blocks.TextBlock(
                        max_length=999,
                        required=False,
                        help_text="To highlight the word into red please put it inside these tags: <b>…text…</b>",
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/slider.html"
        icon = "image / picture"
        label = "Banners-Slider"


class CategoryCarousel(blocks.StructBlock):
    title = blocks.CharBlock(max_length=150, required=False)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("category_title", blocks.CharBlock(required=False)),
                ("image", ImageChooserBlock(required=False)),
                ("image_alt", blocks.CharBlock(max_length=255, required=False)),
                ("page_link", blocks.CharBlock(required=False, help_text="Use <location_slug> to insert location slug")),
                ("button_text", blocks.CharBlock(max_length=255, required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/category_carousel.html"
        icon = "image / picture"
        label = "Browse By Category Carousel"


class CallToActionBlock(blocks.StructBlock):
    title = blocks.TextBlock(
        required=False,
        help_text="To highlight the word into red please put it inside these tags: <b>…text…</b>",
    )
    text = blocks.TextBlock(required=False, help_text="Add additional text")
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn More", max_length=55)
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    background_image_alt = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/cta_block.html"
        icon = "link"
        label = "Call to Action"


class RecentWorksBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=250, blank=True)
    background_color_grey = blocks.BooleanBlock(default=False, required=False)
    works = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=False)),
                ("image_alt", blocks.CharBlock(max_length=255, required=False)),
                ("link_title", blocks.CharBlock(required=False, max_length=100)),
                ("link", blocks.CharBlock(max_length=255, required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/recent_works.html"
        icon = "placeholder"
        label = "Recent Works"


class SocialIconBanner(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default="Join The TrailersPlus Community")
    text = blocks.CharBlock(
        required=False, default="Stay Up to Date With the Latest and Greatest"
    )
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock()
    background_image_alt = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/social_icons_banner.html"
        icon = "list-ul"
        label = "Social Icons Block"


class PartnersBlock(blocks.StaticBlock):
    class Meta:
        template = "streams/partners_block.html"
        icon = "group"
        label = "Partners Block"


class BannersLink(blocks.StructBlock):
    title_left_banner = blocks.CharBlock(required=False)
    sub_title_left_banner = blocks.CharBlock(required=False)
    image_left_banner = ImageChooserBlock()
    background_image_alt_left = blocks.CharBlock(max_length=255, required=False)
    left_banner_link_url = blocks.CharBlock(max_length=500, blank=True)

    title_right_banner = blocks.CharBlock(required=False)
    sub_title_right_banner = blocks.CharBlock(required=False)
    image_right_banner = ImageChooserBlock()
    background_image_alt_right = blocks.CharBlock(max_length=255, required=False)
    right_banner_link_url = blocks.CharBlock(max_length=500, blank=True)

    class Meta:
        template = "streams/banners_link.html"
        icon = "image / picture"
        label = "Two Pictures Block"


class BigTextSection(blocks.StructBlock):
    text_block_top = blocks.TextBlock(required=False, help_text="Use \"<count\" to insert stores quantity automatically. Ex. \"We have <count> stores\" --> \"We have 22 stores\"")
    text_block_top_subtext = blocks.TextBlock(max_length=999, required=False)
    text_block_bottom_subtext = blocks.TextBlock(max_length=999, required=False)

    class Meta:
        template = "streams/big_text_section.html"
        icon = "title"
        label = "Big Text Section"


class BigBanner(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    background_image_alt = blocks.CharBlock(max_length=255, required=False)
    title = blocks.CharBlock(required=False, max_length=200)
    text = blocks.TextBlock(required=False, max_length=1000, help_text="Optional")
    buttons = blocks.ListBlock(
        blocks.StructBlock(
            [
                (
                    "button_icon",
                    ImageChooserBlock(
                        required=False, help_text="Icon for Button(Optional)"
                    ),
                ),
                ("button_title", blocks.CharBlock(required=False, max_length=255)),
                ("button_link", blocks.CharBlock(max_length=999, required=False)),
                ("open_in_new_tab", blocks.BooleanBlock(required=False)),
            ],
        )
    )

    class Meta:
        template = "streams/big_banner_block.html"
        icon = "image / picture"
        label = "Big Banner & Buttons"


class CarouselPopup(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=150)
    parts = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("popup_id", blocks.IntegerBlock()),
                ("title", blocks.CharBlock(max_length=200)),
                ("description", blocks.TextBlock(required=False, max_length=1000)),
                ("price", blocks.TextBlock(required=False)),
                ("main_image", ImageChooserBlock(required=False)),
                (
                    "gallery_images",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [("image", ImageChooserBlock(required=False))]
                        )
                    ),
                ),
                (
                    "options",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [("option", blocks.RichTextBlock(required=False))]
                        )
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/carousel_popup.html"
        icon = "image / picture"
        label = "Carousel & PopUp"


class PartsAndAccessoriesBlock(blocks.StructBlock):
    tabs = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("tab_title", blocks.CharBlock()),
                (
                    "items",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("title", blocks.CharBlock()),
                                ("image", ImageChooserBlock()),
                                (
                                    "link_url",
                                    blocks.CharBlock(max_length=999, required=False),
                                ),
                            ]
                        )
                    ),
                ),
            ]
        ),
    )

    class Meta:
        template = "streams/popular_parts_tabs.html"
        icon = "image / picture"
        label = "Popular Parts Tab"


class RightSideBlogBanner(blocks.StructBlock):
    banners = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("sub_title", blocks.CharBlock(max_length=255, required=False)),
                ("image", ImageChooserBlock(required=False)),
                ("image_alt", blocks.CharBlock(max_length=255, required=False)),
                ("button_text", blocks.TextBlock(required=False)),
                ("button_link", blocks.PageChooserBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/rightside_blog_banner.html"
        icon = "image / picture"
        label = "RightSide Blog Banner"


class NextPreviousPostsS(blocks.StaticBlock):
    next_text_button = blocks.CharBlock(max_length=255, required=False)
    previous_text_button = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/next_previous_post_block.html"
        icon = "placeholder"
        label = "Next-Previous Posts Block1"


class NextPreviousPostsSt(blocks.StructBlock):
    next_text_button = blocks.CharBlock(max_length=255, required=False)
    previous_text_button = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/next_previous_post_block.html"
        icon = "placeholder"
        label = "Next-Previous Posts Block Final"


class TrustPilotWidget(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.CharBlock(max_length=511, required=False, help_text="Use <b>...</b> for red bg")
    rating = blocks.FloatBlock(required=False, min_value=0, max_value=5, default=0)
    background_grey_color = blocks.BooleanBlock(default=False, required=False)
    is_my_store_page = blocks.BooleanBlock(default=False, required=False)
    columns_layout = blocks.BooleanBlock(default=False, required=False)

    class Meta:
        template = "streams/trustpilot.html"
        icon = "group"
        label = "TrustPilot Widget"


class TrustPilotWidgetHorizontal(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.CharBlock(max_length=511, required=False, help_text="Use <b>...</b> for red bg")
    bottom_title = blocks.CharBlock(max_length=511, required=False, help_text="Use <b>...</b> for red bg")
    rating = blocks.FloatBlock(required=False, min_value=0, max_value=5, default=0)
    background_grey_color = blocks.BooleanBlock(default=False, required=False)
    is_my_store_page = blocks.BooleanBlock(default=False, required=False)
    columns_layout = blocks.BooleanBlock(default=False, required=False)
    paddings = blocks.BooleanBlock(default=False, required=False)

    class Meta:
        template = "streams/trustpilot_horizontal.html"
        icon = "group"
        label = "TrustPilot Widget Horizontal"


class RichtextBlock(blocks.RichTextBlock):
    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "RichText"


class RichtextBlockPlus(blocks.StructBlock):
    richtext_plus = blocks.TextBlock(
        required=False,
        help_text='HTML+',
    )

    class Meta:
        template = "streams/richtext_plus.html"
        icon = "doc-full"
        label = "RichText Plus"


class SingleImage(blocks.StructBlock):
    single_image = ImageChooserBlock()
    single_image_alt = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/single_image.html"
        icon = "image / picture"
        label = "Single Image"


class ShareBtn(blocks.CharBlock):
    button_title = blocks.CharBlock(max_length=99, default="Share this", required=False)

    class Meta:
        template = "streams/share_btns.html"
        icon = "placeholder"
        label = "Share Button"


class CallUsBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=255, required=False)
    sub_text = blocks.TextBlock(
        required=False,
        help_text='For example: Please call us at <b><a href="tel:+1877-850-7587">877-850-7587</a></b> to discuss!',
    )

    class Meta:
        template = "streams/call_us_block.html"
        icon = "placeholder"
        label = "Call Us Text Section 1"


class YoutubeEmbedBlock(EmbedBlock):
    class Meta:
        template = "streams/embed_youtube.html"
        icon = "media"
        label = "YouTube Video"


class DividerLine(blocks.StaticBlock):
    class Meta:
        template = "streams/divider.html"
        icon = "placeholder"
        label = "Divider Line"


# SEARCH AND REPAIR PAGE


class ServiceAndRepairBanner(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock()
    background_image_alt = blocks.CharBlock(required=False, max_length=255)

    label_image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.CharBlock(max_length=500, required=False)
    text = blocks.TextBlock(max_length=1000, required=False)
    icon_image = ImageChooserBlock(required=False)

    class Meta:
        template = "streams/service_and_repair_banner.html"
        icon = "placeholder"
        label = "Service and Repair Banner"


class BeforeAfterSlider(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=150)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image_before", ImageChooserBlock()),
                ("image_after", ImageChooserBlock()),
            ]
        )
    )
    text_button_before = blocks.CharBlock(max_length=55, required=False)
    text_button_after = blocks.CharBlock(max_length=55, required=False)

    slider_tables = blocks.ListBlock(
        blocks.StructBlock(
            [
                (
                    "slider_row",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                (
                                    "slider_item_title",
                                    blocks.CharBlock(max_length=255, required=False),
                                ),
                            ]
                        )
                    ),
                )
            ]
        )
    )

    class Meta:
        template = "streams/before_after_slider.html"
        icon = "image / picture"
        label = "Before & After Slider"


class TableRow(blocks.StructBlock):
    tables = blocks.ListBlock(
        blocks.StructBlock(
            [
                (
                    "row",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                (
                                    "item_title",
                                    blocks.CharBlock(max_length=255, required=False),
                                ),
                            ]
                        )
                    ),
                )
            ]
        )
    )

    class Meta:
        template = "streams/table_row.html"
        icon = "list-ul"
        label = "Table Row"


class CallNowBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=255, required=False)
    sub_text = blocks.CharBlock(max_length=255, required=False)
    phone = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/call_now_block.html"
        icon = "placeholder"
        label = "Call Us Text Section 2"


# STORE FINDER


class StoreFinderMap(blocks.StructBlock):
    h3_title = blocks.CharBlock(max_length=255, required=False, help_text="Use \"<count\" to insert stores quantity automatically. Ex. \"We have <count> stores\" --> \"We have 22 stores\"")
    h1_title = blocks.CharBlock(max_length=255, required=False)
    find_stores_text = blocks.CharBlock(max_length=255, required=False)
    my_stores_text = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/store_finder_map.html"
        icon = "view"
        label = "Store Finder Map"


# FLEET SALES


class FleetSalesBanner(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    bottom_logo = ImageChooserBlock(required=False, help_text="Optional")
    background_image_alt = blocks.CharBlock(required=False, max_length=255)
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(
        required=False,
        help_text="To highlight the word into red please put it inside these tags: <b>…text…</b>",
    )
    textarea = blocks.TextBlock(required=False, help_text="Optional - <p>")
    overlay = blocks.IntegerBlock(
        default=2, required=False, min_value=1, max_value=5, help_text="Min: 1, Max: 5"
    )
    float_left = blocks.BooleanBlock(default=False, required=False)

    class Meta:
        template = "streams/fleet_sales_banner.html"
        icon = "image / picture"
        label = "Fleet Sales Banner"


class TextBlock(blocks.TextBlock):
    class Meta:
        template = "streams/text_block.html"
        icon = "title"
        label = "Text Block"


class H2Title(blocks.StructBlock):
    title = blocks.CharBlock(max_length=500)
    sub_title = blocks.TextBlock(required=False, help_text="Optional")

    class Meta:
        template = "streams/h2_title.html"
        icon = "title"
        label = "H2 Title"


class H3Title(blocks.CharBlock):
    class Meta:
        template = "streams/h3_title.html"
        icon = "title"
        label = "H3 Title"


class WhyChooseUs(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    image_align_center = blocks.BooleanBlock(default=False, required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)
    items = blocks.ListBlock(blocks.StructBlock([("item_text", blocks.CharBlock()), ]))

    class Meta:
        template = "streams/why_choose_us.html"
        icon = "title"
        label = "Why Choose Us Block"


class CaseStudiesCarousel(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [("item_image", ImageChooserBlock()), ("item_text", blocks.TextBlock()), ]
        )
    )

    class Meta:
        template = "streams/case_studies.html"
        icon = "image / picture"
        label = "Case Studies Block"


class LearnMoreBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("item_image", ImageChooserBlock()),
                ("item_text", blocks.TextBlock()),
                ("item_link", blocks.PageChooserBlock()),
            ]
        )
    )

    class Meta:
        template = "streams/learn_more.html"
        icon = "image / picture"
        label = "Learn More Block"


class WhyWaitBlock(blocks.StructBlock):
    title = blocks.TextBlock(
        max_length=255,
        required=False,
        help_text="To highlight the word into red please put it inside these tags: <b>…text…</b>",
    )
    sub_title = blocks.TextBlock(required=False)
    richtext = blocks.TextBlock(required=False)

    free_inspection_icon = ImageChooserBlock(required=False)
    free_inspection_title = blocks.CharBlock(max_length=255, required=False)
    free_inspection_text = blocks.TextBlock(required=False)
    free_inspection_link = blocks.CharBlock(
        required=False, help_text="http:// or https:// is required !"
    )

    image = ImageChooserBlock(required=False)

    class Meta:
        template = "streams/why_wait_block.html"
        icon = "placeholder"
        label = "Why Wait Block"


class WhyWaitBlockV2(blocks.StructBlock):
    title = blocks.TextBlock(
        max_length=255,
        required=False,
        help_text="To highlight the word into red please put it inside these tags: <b>…text…</b>",
    )
    sub_title = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    image_mobile = ImageChooserBlock(required=False)

    class Meta:
        template = "streams/why_wait_block_v2.html"
        icon = "placeholder"
        label = "Why Wait Block V2"


# TIRE WARRANTYF


class ImageAndText(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    text = blocks.TextBlock(required=False)

    class Meta:
        template = "streams/image_and_text_block.html"
        icon = "image / picture"
        label = "Image+Text Block"


class ImageGallery(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255)
    block_id = blocks.CharBlock(required=False, max_length=55)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("caption", blocks.CharBlock(max_length=255, required=False)),
                (
                    "sub_caption",
                    blocks.CharBlock(
                        max_length=999, required=False, help_text="Optional"
                    ),
                ),
            ]
        )
    )
    text = blocks.TextBlock(required=False, help_text="Optional")
    scroll_button_text = blocks.CharBlock(required=False)
    scroll_button_link = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/image_gallery.html"
        icon = "image / picture"
        label = "Image Gallery"


class ImageGalleryV2(blocks.StructBlock):
    main_title = blocks.CharBlock(max_length=500, required=False, help_text='Optional')
    main_sub_title = blocks.TextBlock(required=False, help_text="Optional")
    title = blocks.TextBlock(required=False)
    block_id = blocks.CharBlock(required=False, max_length=55)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("caption", blocks.CharBlock(max_length=255, required=False)),
                ("sub_caption", blocks.TextBlock(required=False, help_text="Optional")),
            ]
        )
    )
    scroll_button_text = blocks.CharBlock(required=False)
    scroll_button_link = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/image_gallery_2.html"
        icon = "image / picture"
        label = "Image Gallery V2"


class CallUsToday(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    logo = ImageChooserBlock(required=False)
    title = blocks.TextBlock(
        required=False,
        help_text='For example: Please call us at <b><a href="tel:+1877-850-7587">877-850-7587</a></b> to discuss!',
    )

    class Meta:
        template = "streams/call_us_today.html"
        icon = "image / picture"
        label = "Call Us Banner+Text"


class BigBannerV2(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    logo = ImageChooserBlock(required=False)
    title = blocks.TextBlock(
        required=False,
        help_text='For example: Please call us at <b><a href="tel:+1877-850-7587">877-850-7587</a></b> to discuss!',
    )
    sub_title = blocks.TextBlock(required=False, help_text="Optional")

    class Meta:
        template = "streams/call_us_banner_v2.html"
        icon = "image / picture"
        label = "Big Banner+Text V2"


class BannerBreadCrumbs(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    overlay = blocks.IntegerBlock(
        default=2, required=False, min_value=1, max_value=5, help_text="Min: 1, Max: 5"
    )
    bg_fill = blocks.BooleanBlock(required=False, help_text='Optional! Background Fill class for block.')
    title = blocks.CharBlock(max_length=255, required=False)
    breadcrumbs_first = blocks.CharBlock(max_length=255, required=False)
    breadcrumbs_last = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/banner_and_breadcrumbs.html"
        icon = "image / picture"
        label = "Banner + Breadcrumbs"


class ButtonsBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    section_description = blocks.TextBlock(required=False, help_text="Optional")
    buttons = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("button_title", blocks.CharBlock(max_length=255)),
                (
                    "button_link",
                    blocks.CharBlock(
                        required=False,
                        help_text='Example link: "https://google.com" or use #id',
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/buttons_block.html"
        icon = "placeholder"
        label = "Buttons Block"


class ModelsWeOfferBlock(blocks.StructBlock):
    block_id = blocks.CharBlock(max_length=55, required=False)
    main_title = blocks.CharBlock(max_length=500, required=False, help_text='Optional')
    main_sub_title = blocks.TextBlock(required=False, help_text="Optional")
    title = blocks.CharBlock(max_length=255, required=False)
    models = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("model_image", ImageChooserBlock()),
                ("model_title", blocks.CharBlock(required=False)),
                ("opacity", blocks.BooleanBlock(required=False, help_text='Optional! Opacity for block.')),
                (
                    "items",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [("title", blocks.CharBlock(required=False)), ]
                        )
                    ),
                ),
            ]
        ),
    )

    class Meta:
        template = "streams/models_offer_list.html"
        icon = "placeholder"
        label = "Models We Offer List"


class TrailersSizeBlock(blocks.StructBlock):
    section_title = blocks.CharBlock(max_length=255)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255)),
                ("description", blocks.TextBlock(max_length=2000, required=False)),
                ("size_title", blocks.CharBlock(max_length=255, required=False)),
                ("size_description", blocks.TextBlock(max_length=2000, required=False)),
                ("first_image", ImageChooserBlock()),
                ("second_image", ImageChooserBlock()),
                ("button_link", blocks.CharBlock(required=False)),
                ("button_text", blocks.TextBlock(required=False)),
                ("reverse_align", blocks.BooleanBlock(default=False, required=False)),
                (
                    "block_id",
                    blocks.CharBlock(
                        required=False, help_text="Optional for Buttons Block"
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/trailer_size_block.html"
        icon = "image / picture"
        label = "TrailerSize Block"


class TextAreaBackgroundImage(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    text = blocks.TextBlock(required=False)

    class Meta:
        template = "streams/text_background_image.html"
        icon = "title"
        label = "TextArea + Background Image"


class YoutubeBanner(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    text_area_1 = blocks.TextBlock(required=False)
    text_area_2 = blocks.TextBlock(required=False)
    youtube_link = blocks.CharBlock()

    background_image_logo = ImageChooserBlock(required=False, help_text="Optional")

    class Meta:
        template = "streams/video_banner.html"
        icon = "media"
        label = "YouTube Banner"


class ImageIconNavigationBlock(blocks.StructBlock):
    navigation = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255)),
                ("link", blocks.CharBlock(help_text="Paste URL or ID to Block")),
            ]
        )
    )
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("icon", ImageChooserBlock()),
                ("title", blocks.CharBlock(required=False)),
                ("sub_title", blocks.CharBlock(required=False)),
                ("textarea", blocks.TextBlock(required=False)),
                (
                    "block_id",
                    blocks.TextBlock(
                        required=False,
                        help_text="Optional. Use this field for Navigation Links above",
                    ),
                ),
                ("reverse", blocks.BooleanBlock(required=False, default=False)),
            ]
        )
    )

    class Meta:
        template = "streams/image_icon_block.html"
        icon = "image / picture"
        label = "Image Block + ID Navigation"


class WhyBuyYoutube(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image_preview", ImageChooserBlock()),
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("youtube_link", blocks.CharBlock()),
            ]
        )
    )

    class Meta:
        template = "streams/why_buy_youtube.html"
        icon = "media"
        label = "Why Buy YouTube"


class BlockquotesReview(blocks.StructBlock):
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("review", blocks.TextBlock()),
                ("author_name", blocks.CharBlock(max_length=255, required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/blockquotes_reviews.html"
        icon = "openquote"
        label = "Blockquotes-Reviews Block"


class CallToActionV2(blocks.StructBlock):
    title = blocks.TextBlock()
    button_text = blocks.TextBlock()
    button_link = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/call_to_action_v2.html"
        icon = "placeholder"
        label = "Call To Action V2"


class ArticleSidebar(blocks.StructBlock):
    article_title = blocks.CharBlock(max_length=255)
    article_text = RichtextBlock(
        features=[
            "h2",
            "h3",
            "h4",
            "h5",
            "bold",
            "italic",
            "link",
            "ul",
            "t-center",
            "font-underline",
        ]
    )

    addresses = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255)),
                (
                    "items",
                    blocks.ListBlock(
                        blocks.StructBlock([("address", blocks.RichTextBlock()), ])
                    ),
                ),
            ]
        )
    )
    manuals = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255)),
                (
                    "items",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("image", ImageChooserBlock()),
                                ("text", blocks.TextBlock(required=False)),
                                ("button_link", blocks.CharBlock(required=False)),
                                (
                                    "button_text",
                                    blocks.CharBlock(max_length=255, required=False),
                                ),
                            ]
                        )
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/article_sidebar.html"
        icon = "cogs"
        label = "Article + Sidebar"


class ImagesTextBlocks(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)

    right_block = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255, required=False, help_text="Use \"<count\" to insert stores quantity automatically. Ex. \"We have <count> stores\" --> \"We have 22 stores\"")),
                ("textarea", blocks.TextBlock(required=False)),
                ("image", ImageChooserBlock(required=False)),
            ]
        )
    )
    left_block = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("textarea", blocks.TextBlock(required=False)),
                ("image", ImageChooserBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/our_team_images_block.html"
        icon = "image / picture"
        label = "Images + Text Block"


class ImagesCarousel(blocks.StructBlock):
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("textarea", blocks.TextBlock(required=False)),
                ("image", ImageChooserBlock()),
            ]
        )
    )

    class Meta:
        template = "streams/our_team_carousel.html"
        icon = "image / picture"
        label = "OurTeam Image Carousel"


class ServiceIconsBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=255, required=False)

    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("icon", ImageChooserBlock()),
                ("title", blocks.CharBlock(max_length=255)),
                ("textarea", blocks.TextBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/service_icons_block.html"
        icon = "image / picture"
        label = "Certified Icons Block"


class CheckpointList(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    sub_title = blocks.TextBlock(required=False)

    list_blocks = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255)),
                (
                    "list_items",
                    blocks.ListBlock(
                        blocks.StructBlock([("item", blocks.TextBlock()), ])
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/checkpoint_list.html"
        icon = "list-ul"
        label = "CheckPoints Block"


class CallUsTodayV2(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(max_length=255)
    sub_title = blocks.TextBlock(required=False)

    items = blocks.ListBlock(
        blocks.StructBlock([("item", blocks.TextBlock(required=False))])
    )

    class Meta:
        template = "streams/call_us_today_v2.html"
        icon = "snippet"
        label = "Call Us Today V2"


class ReturnPolicy(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    textarea = RichtextBlock(
        features=[
            "h2",
            "h3",
            "h4",
            "h5",
            "bold",
            "italic",
            "link",
            "ul",
            "t-center",
            "font-underline",
        ]
    )

    class Meta:
        template = "streams/policy_block.html"
        icon = "title"
        label = "Return Policy Block"


class ContactUsBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)
    phone = blocks.TextBlock(required=False)

    column_left = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("sub_title", blocks.TextBlock(required=False)),
                ("textarea", blocks.TextBlock(required=False)),
                (
                    "social_links",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("title", blocks.CharBlock(required=False)),
                                ("link", blocks.CharBlock(required=False)),
                                (
                                    "icon",
                                    blocks.CharBlock(
                                        required=False,
                                        help_text='Use Font Awesome Icons names. For example: "fa fa-facebook".',
                                    ),
                                ),
                                (
                                    "icon_class",
                                    blocks.CharBlock(
                                        required=False,
                                        help_text="Optional! For example - 'social-icon--ig or social-icon--fb'",
                                    ),
                                ),
                            ]
                        )
                    ),
                ),
            ]
        )
    )

    column_right = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=255)),
                (
                    "rows",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                (
                                    "text_block",
                                    blocks.ListBlock(
                                        blocks.StructBlock(
                                            [
                                                (
                                                    "title",
                                                    blocks.CharBlock(
                                                        max_length=255, required=False
                                                    ),
                                                ),
                                                (
                                                    "textarea",
                                                    blocks.TextBlock(required=False),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        )
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/contact_us.html"
        icon = "title"
        label = "Contact Us Section"


class FinancingCards(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("caption", blocks.TextBlock(required=False)),
                ("button_link", blocks.CharBlock(required=False)),
                ("button_text", blocks.CharBlock(required=False)),
            ]
        )
    )
    benefits_title = blocks.CharBlock(max_length=255, required=False)
    benefits = blocks.ListBlock(
        blocks.StructBlock(
            [
                (
                    "items_list",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                (
                                    "item",
                                    blocks.CharBlock(max_length=255, required=False),
                                ),
                            ]
                        )
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/financing_cards.html"
        icon = "snippet"
        label = "Financing Cards Block"


class OptionsBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    options = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("icon", ImageChooserBlock()),
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("textarea", blocks.TextBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/options_section.html"
        icon = "snippet"
        label = "Options Block"


class OptionsBlockV2(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    options = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("icon", ImageChooserBlock()),
                ("title", blocks.CharBlock(max_length=255, required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/options_section_v2.html"
        icon = "snippet"
        label = "Options Block V2"


class VacanciesSection(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    vacancies = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("state", blocks.CharBlock(max_length=255)),
                (
                    "items",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("vacancy_title", blocks.CharBlock(max_length=255)),
                                (
                                    "city",
                                    blocks.CharBlock(max_length=255, required=False),
                                ),
                                (
                                    "button_link",
                                    blocks.CharBlock(
                                        required=False,
                                        help_text="http:// or https:// is required !",
                                    ),
                                ),
                                (
                                    "button_text",
                                    blocks.CharBlock(max_length=255, required=False),
                                ),
                            ]
                        )
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "streams/careers_section.html"
        icon = "title"
        label = "Careers Block"


class ResourcesBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("textarea", blocks.TextBlock(required=False)),
                (
                    "button_link",
                    blocks.CharBlock(
                        required=False, help_text="http:// or https:// is required !"
                    ),
                ),
                ("button_text", blocks.CharBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/resources_section.html"
        icon = "snippet"
        label = "Resources Block"


class AboutUsImagesTextButton(blocks.StructBlock):
    image = ImageChooserBlock()
    image_reverse = blocks.BooleanBlock(default=False, required=False)
    title = blocks.CharBlock(max_length=255)
    textarea = blocks.TextBlock(required=False)
    text_align = blocks.CharBlock(
        required=False, default="left", help_text='Paste "left" or "right" here!'
    )
    button_link = blocks.CharBlock(required=False, help_text="http:// or https:// is required !")
    button_text = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/about_us_images_text.html"
        icon = "image / picture"
        label = "AboutUs Image+Text Block"








class TrailersOfferImagesBlocks(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("title", blocks.CharBlock(max_length=255, required=False)),
                ("textarea", blocks.TextBlock(required=False)),
                ("view_button_text", blocks.TextBlock(required=False)),
                ("view_button_link", blocks.CharBlock(required=False, help_text="http:// or https:// is required !")),
                ("information_button_text", blocks.TextBlock(required=False)),
                ("information_button_link", blocks.CharBlock(required=False, help_text="http:// or https:// is required !")),
            ]
        )
    )

    class Meta:
        template = "streams/trailers_offer_image_blocks.html"
        icon = "image / picture"
        label = "TrailersWeOffer Image Block"


class CustomerInfoForm(blocks.StructBlock):
    title = blocks.CharBlock(max_length=50, required=False)
    first_name_placeholder = blocks.CharBlock(max_length=50, required=False)
    last_name_placeholder = blocks.CharBlock(max_length=50, required=False)
    company_placeholder = blocks.CharBlock(max_length=50, required=False)
    phone_placeholder = blocks.CharBlock(max_length=50, required=False)
    email_address_placeholder = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        icon = "form"


class PaymentInfoForm(blocks.StructBlock):
    title = blocks.CharBlock(max_length=50, required=False)
    billing_address_placeholder = blocks.CharBlock(max_length=50, required=False)
    city_placeholder = blocks.CharBlock(max_length=50, required=False)
    state_placeholder = blocks.CharBlock(max_length=50, required=False)
    zip_code_placeholder = blocks.CharBlock(max_length=50, required=False)
    card_number_placeholder = blocks.CharBlock(max_length=50, required=False)
    cvv_code_placeholder = blocks.CharBlock(max_length=50, required=False)
    expiry_placeholder = blocks.CharBlock(max_length=50, required=False)
    i_accept_policy_text = blocks.CharBlock(max_length=50, required=False)
    return_refund_text = blocks.CharBlock(max_length=175, required=False)

    class Meta:
        icon = "form"


class ConfirmationForm(blocks.StructBlock):
    title = blocks.CharBlock(max_length=50, required=False)
    pay_now_button_text = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        icon = "tick"


class TrailerCheckoutBlock(blocks.StructBlock):
    sale_price_text = blocks.CharBlock(max_length=50, required=False)
    financing_available_from_text = blocks.CharBlock(max_length=100, required=False)
    tax_changes_text = blocks.CharBlock(max_length=100, required=False)
    delivery_rules = blocks.CharBlock(max_length=255, required=False)
    located_at_text = blocks.CharBlock(max_length=100, required=False)
    get_direction_text = blocks.CharBlock(max_length=50, required=False)
    shipping_quote = blocks.CharBlock(max_length=70, required=False)

    class Meta:
        icon = "doc-full"


class CheckoutBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    customer_info_form = CustomerInfoForm()
    payment_info_form = PaymentInfoForm()
    confirmation_form = ConfirmationForm()
    form_error_message = blocks.CharBlock(max_length=100, required=False)
    back_text = blocks.CharBlock(max_length=50, required=False)
    continue_text = blocks.CharBlock(max_length=50, required=False)
    right_trailer_block = TrailerCheckoutBlock()

    class Meta:
        template = "streams/checkout.html"
        icon = "site"
        label = "CheckoutForm"


class TrailersOfferOptionsLinks(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    option_1 = blocks.CharBlock(max_length=255, required=False)
    option_1_link = blocks.CharBlock(required=False)
    option_2 = blocks.CharBlock(max_length=255, required=False)
    option_2_link = blocks.CharBlock(required=False)
    option_3 = blocks.CharBlock(max_length=255, required=False)
    option_3_link = blocks.CharBlock(required=False)
    option_4 = blocks.CharBlock(max_length=255, required=False)
    option_4_link = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/trailers_offer_options_block.html"
        icon = "list-ul"
        label = "TrailersWeOffer Options SVG"


class BannerSearch(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=355, required=False)
    textarea = blocks.TextBlock(required=False)
    search_title = blocks.CharBlock(max_length=355, required=False)
    search_count_text = blocks.TextBlock(required=False)
    search_button_text = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/banner_search.html"
        icon = "view"
        label = "Banner + Search"


class WhyServiceTextButton(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    title = blocks.CharBlock(max_length=355, required=False)
    button_text = blocks.CharBlock(max_length=255, required=False)
    button_icon = blocks.CharBlock(required=False, help_text='Optional! Use Font Awesome Icons names. For example: "fa fa-facebook".')
    button_link = blocks.CharBlock(required=False, help_text="http:// or https:// is required !")

    class Meta:
        template = "streams/why_service_text_button.html"
        icon = "title"
        label = "Why Service - Text+Button"


class WhyServiceListButtons(blocks.StructBlock):
    title = blocks.CharBlock(max_length=355, required=False)
    list_items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("item_text", blocks.RichTextBlock(required=False)),
            ]
        )
    )
    buttons = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("button_title", blocks.CharBlock(max_length=255)),
                ("button_icon", blocks.CharBlock(required=False, help_text='Use Font Awesome Icons names. For example: "fa fa-facebook".')),
                ("button_link", blocks.CharBlock(required=False, help_text="http:// or https:// is required !")),
            ]
        )
    )

    class Meta:
        template = "streams/why_service_list_buttons.html"
        icon = "list-ul"
        label = "Why Service - List+Buttons"


class ReviewsGallery(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    gallery_items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=False)),
                ("location", blocks.CharBlock(required=False)),
                ("description", blocks.TextBlock(required=False)),
                ("button_text", blocks.CharBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/reviews_gallery.html"
        icon = "image / picture"
        label = "Reviews Gallery"


class CheckoutTnxBlock(blocks.StructBlock):
    reserved_message = blocks.CharBlock(max_length=50, required=False)
    long_text = blocks.RichTextBlock(required=False, help_text='Use "<date> for pick up date, <phone> for store phone, <email> for customer email, to insert that values in text dynamically\nEx: "Tnx <email>! Call <phone> till <date>" --> "Tnx example@example.com! Call +1234567890 till June 13, 2077')
    back_button = blocks.CharBlock(max_length=20, required=False)
    confirmation = blocks.CharBlock(max_length=20, required=False)
    pickup = blocks.CharBlock(max_length=20, required=False)
    sale_price = blocks.CharBlock(max_length=30, required=False)
    financing_available = blocks.CharBlock(max_length=50, required=False)

    class Meta:
        template = "streams/thank-you-checkout.html"
        icon = "snippet"


class ErrorBannerBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)

    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.CharBlock(max_length=999, required=False)
    textarea = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock(max_length=255, required=False)
    link = blocks.URLBlock(required=False)
    link_page = blocks.PageChooserBlock(required=False)

    class Meta:
        template = "streams/error_banner.html"
        icon = "image / picture"
