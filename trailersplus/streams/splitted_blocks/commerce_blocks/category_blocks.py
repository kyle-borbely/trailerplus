from wagtail.admin.edit_handlers import FieldRowPanel
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class BannerBlock(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    background_image_alt = blocks.CharBlock(max_length=255, required=False)
    title_start = blocks.CharBlock(max_length=120, required=False, help_text="Aprox. this text \"The best price & selection of trailers in\"")
    guaranteed_translation = blocks.CharBlock(max_length=25, required=False)
    bullets = blocks.ListBlock(
        blocks.CharBlock(max_length=120, required=False)
    )

    class Meta:
        template = "streams/category/banner.html"
        icon = "title"


class ProductsBlock(blocks.StructBlock):
    category_title = blocks.CharBlock(max_length=20, required=False)
    sort_by_title = blocks.CharBlock(max_length=20, required=False)
    price_l_t_h = blocks.CharBlock(max_length=30, required=False, help_text="Price low to high")
    price_h_t_l = blocks.CharBlock(max_length=30, required=False, help_text="Price high to low")
    size_l_t_h = blocks.CharBlock(max_length=30, required=False, help_text="Size low to high")
    size_h_t_l = blocks.CharBlock(max_length=30, required=False, help_text="Size high to low")
    sold_label = blocks.CharBlock(max_length=20, required=False)
    reserved_label = blocks.CharBlock(max_length=20, required=False)
    sale_price = blocks.CharBlock(max_length=20, required=False)

    class Meta:
        template = "streams/category/products.html"
        icon = "grip"


class BulletsBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=120, required=False)
    bullets = blocks.ListBlock(
        blocks.CharBlock(max_length=511, required=False),
        help_text='Use <store> to insert store name automatically. Ex. \"Buy in <store>\" --> \"Buy in TrailersPlus Warrenton,VA\"'
    )

    class Meta:
        template = "streams/category/bullets.html"
        icon = "doc-full"