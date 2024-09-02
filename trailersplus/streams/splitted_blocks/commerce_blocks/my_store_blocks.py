from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class BannerBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    background_image_alt = blocks.CharBlock(max_length=255, required=False)
    title = blocks.CharBlock(max_length=100, required=False)
    description = blocks.TextBlock(required=False)

    class Meta:
        template = "streams/my_store/banner.html"
        icon = "title"


class DirectionsBlock(blocks.StructBlock):
    view_inventory = blocks.CharBlock(max_length=50, required=False)
    get_directions = blocks.CharBlock(max_length=50, required=False)
    store_hours = blocks.CharBlock(max_length=50, required=False)
    learn_why_appointment = blocks.CharBlock(max_length=100, required=False)

    class Meta:
        template = "streams/my_store/directions.html"
        icon = "redirect"


class ProductsBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False, help_text="Use \"<count>\" to insert trailer count and \"<store>\" to insert store name\nEx: \"<count> Trailers in <store>\" --> \"105 Trailers in Amarillo, TX\"")
    in_stock = blocks.CharBlock(max_length=30, required=False)
    as_low_as = blocks.CharBlock(max_length=30, required=False)

    class Meta:
        template = "streams/my_store/products.html"
        icon = "snippet"


class LongTextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(required=False, help_text="Use \"<phone>\" to insert phone automatically. Ex: \"Call us <phone>\" --> \"Call us (877) 850-7587. This tag will add tel link")

    class Meta:
        template = "streams/my_store/long_text.html"
        icon = "doc-full"


class CallTodayBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    background_image_alt = blocks.CharBlock(max_length=255, required=False)
    somewhy_happy_guy_image = ImageChooserBlock()
    somewhy_happy_guy_image_alt = blocks.CharBlock(max_length=255, required=False)
    title = blocks.CharBlock(max_length=255, required=False)
    call_today = blocks.CharBlock(max_length=30, required=False)
    points = blocks.ListBlock(
        blocks.CharBlock(max_length=100, required=False)
    )

    class Meta:
        template = "streams/my_store/call_today.html"
        icon = "snippet"


class CustomerReviewsBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_alt = blocks.CharBlock(max_length=255, required=False)
    reviews_title = blocks.CharBlock(max_length=50, required=False)
    reviews = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("review_text", blocks.TextBlock(required=False)),
                ("review_author", blocks.CharBlock(max_length=50, required=False)),
            ]
        )
    )
    about_title = blocks.CharBlock(max_length=50, required=False)
    about_text = blocks.TextBlock(required=False)

    class Meta:
        template = "streams/my_store/customer_reviews.html"
        icon = "user"


class OneStopShopBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, required=False)
    bullets = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("icon", ImageChooserBlock()),
                ("icon_alt", blocks.CharBlock(max_length=50, required=False)),
                ("title", blocks.CharBlock(max_length=100, required=False)),
                ("text", blocks.TextBlock()),
            ]
        )
    )

    class Meta:
        template = "streams/my_store/one_stop.html"
        icon = "list-ul"


class GetDirections(blocks.StructBlock):
    go_to_google_maps = blocks.CharBlock(max_length=30, required=False)
    directions = blocks.CharBlock(max_length=20, required=False)

    class Meta:
        template = "streams/my_store/directions_popup.html"
        icon = "redirect"
