from wagtail.core import blocks


class ProductList(blocks.StructBlock):
    main_section_title = blocks.CharBlock(max_length=255, required=False)
    filter_title = blocks.CharBlock(max_length=30, required=False)
    filter_location = blocks.CharBlock(max_length=30,  required=False)
    filter_types = blocks.CharBlock(max_length=30, required=False)
    filter_length = blocks.CharBlock(max_length=30, required=False)
    filter_price = blocks.CharBlock(max_length=30, required=False)
    close_filter = blocks.CharBlock(max_length=30, required=False)
    trailers_available = blocks.TextBlock(required=False)
    trailers_special = blocks.CharBlock(max_length=30, required=False)
    trailers_reserved = blocks.CharBlock(max_length=30, required=False)
    trailers_sold = blocks.CharBlock(max_length=30, required=False)
    no_trailers_available = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/inventory/product_list.html"
        icon = "snippet"
        label = "Product List"


class AdditionalMessage(blocks.StructBlock):
    message_text = blocks.TextBlock()

    class Meta:
        template = "streams/inventory/additional_message.html"
        icon = "warning"
