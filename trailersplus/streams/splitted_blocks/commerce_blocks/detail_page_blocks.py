from wagtail.admin.edit_handlers import FieldRowPanel
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class ProductPage(blocks.StructBlock):
    back_to_inventory_text = blocks.TextBlock(required=False)
    mail_text = blocks.CharBlock(max_length=55, required=False)
    print_text = blocks.CharBlock(max_length=55, required=False)
    sale_price_text = blocks.CharBlock(required=False)
    found_it_lower_text = blocks.CharBlock(required=False)
    get_off_sale_text = blocks.CharBlock(required=False, help_text="Use <off_price> to insert off price automatically. EX. \"Get <off_price>$ off\" --> \"Get 50$ off\"")
    financing_available_text = blocks.TextBlock(required=False)
    schedule_an_appointment_button_text = blocks.CharBlock(required=False)
    reserve_trailer_button_text = blocks.CharBlock(required=False)
    add_to_cart_button_text = blocks.CharBlock(required=False)
    trailer_located_at_text = blocks.CharBlock(required=False)
    get_direction_text = blocks.CharBlock(required=False)
    free_delivery_text = blocks.TextBlock(required=False)
    why_we_are_appointment_text = blocks.CharBlock(required=False)
    specifications_text = blocks.CharBlock(required=False)
    trailer_details_text = blocks.CharBlock(required=False)
    color_text = blocks.CharBlock(required=False)
    size_text = blocks.CharBlock(required=False)
    tires_text = blocks.CharBlock(required=False)
    coupler_text = blocks.CharBlock(required=False)
    features_text = blocks.CharBlock(required=False)
    clearance_lights_text = blocks.CharBlock(required=False)
    tail_lights_text = blocks.CharBlock(required=False)
    undercoating_text = blocks.CharBlock(required=False)
    dimensions_text = blocks.CharBlock(required=False)
    overall_length_text = blocks.CharBlock(required=False)
    overall_width_text = blocks.CharBlock(required=False)
    overall_height_text = blocks.CharBlock(required=False)
    interior_length_text = blocks.CharBlock(required=False)
    interior_width_text = blocks.CharBlock(required=False)
    interior_height_text = blocks.CharBlock(required=False)
    rear_door_height_text = blocks.CharBlock(required=False)
    rear_door_width_text = blocks.CharBlock(required=False)
    axles_and_brakes_text = blocks.CharBlock(required=False)
    empty_weight_text = blocks.CharBlock(required=False)
    suspensions_text = blocks.CharBlock(required=False)
    brakes_text = blocks.CharBlock(required=False)
    construction_text = blocks.CharBlock(required=False)
    frame_text = blocks.CharBlock(required=False)
    frame_centers_text = blocks.CharBlock(required=False)
    wall_centers_text = blocks.CharBlock(required=False)
    flooring_text = blocks.CharBlock(required=False)
    walls_text = blocks.CharBlock(required=False)
    nationwide_warranty_text = blocks.CharBlock(required=False)
    overall_text = blocks.CharBlock(required=False)
    roof_text = blocks.CharBlock(required=False)
    axles_text = blocks.CharBlock(required=False)
    tires_warranty_text = blocks.CharBlock(required=False)
    tires_url_text = blocks.RichTextBlock(required=False)
    trailers_reserved = blocks.CharBlock(max_length=30, required=False)
    trailers_sold = blocks.CharBlock(max_length=30, required=False)

    class Meta:
        template = "streams/detail/product_page.html"
        icon = "snippet"
        label = "Product page"


class Schedule(blocks.StructBlock):
    form_title = blocks.CharBlock(max_length=255, required=False)
    form_description = blocks.TextBlock(required=False)
    placeholder_first_name = blocks.CharBlock(max_length=55, required=False)
    placeholder_last_name = blocks.CharBlock(max_length=55, required=False)
    placeholder_phone = blocks.CharBlock(max_length=55, required=False)
    placeholder_email = blocks.CharBlock(max_length=55, required=False)
    policy_accept = blocks.RichTextBlock(required=False)
    button_text = blocks.CharBlock(max_length=255, required=False)
    success_message = blocks.CharBlock(max_length=999, required=False)

    appointment_right_title = blocks.CharBlock(max_length=255, required=False)
    appointment_right_description = blocks.TextBlock(required=False)
    appointment_right_list = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("list_item", blocks.RichTextBlock(required=False))
            ]
        )
    )

    class Meta:
        template = "streams/detail/schedule_popup.html"
        icon = "snippet"
        label = "Schedule"


class Appointment(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)
    item_list = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("item", blocks.RichTextBlock(required=False))
            ]
        )
    )
    textarea = blocks.TextBlock(required=False, help_text='Optional; Use <phone> to insert store phone automatically. Ex. \"Call us <phone>\" --> \"Call us <a href=\'tel:+1123442\'>+1123442</a>')

    class Meta:
        template = "streams/detail/appointment_popup.html"
        icon = "snippet"
        label = "Appointment"


class CTA(blocks.StructBlock):
    background_image = ImageChooserBlock()
    background_image_mobile = ImageChooserBlock(required=False)
    title = blocks.TextBlock(required=False)
    sub_title = blocks.TextBlock(required=False)
    reserve_button_text = blocks.CharBlock(required=False, max_length=255)
    schedule_button_text = blocks.CharBlock(required=False, max_length=255)
    banner_link_text_top = blocks.TextBlock(required=False)
    banner_link_text_bot = blocks.TextBlock(required=False)
    banner_link = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/detail/cta.html"
        icon = "snippet"
        label = "CTA"


class RecentlyViewed(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = "streams/detail/recently_viewed.html"
        icon = "snippet"
        label = "RecentlyViewed"


class LongInfo(blocks.StructBlock):
    textarea = blocks.TextBlock(required=False)

    class Meta:
        template = "streams/detail/long_info.html"
        icon = "snippet"
        label = "LongInfo"


class FoundLower(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, required=False)
    sub_title = blocks.TextBlock(required=False)
    placeholder_website_lower = blocks.CharBlock(max_length=55, required=False)

    form_title = blocks.CharBlock(max_length=255, required=False)
    placeholder_first_name = blocks.CharBlock(max_length=55, required=False)
    placeholder_last_name = blocks.CharBlock(max_length=55, required=False)
    placeholder_phone = blocks.CharBlock(max_length=55, required=False)
    placeholder_email = blocks.CharBlock(max_length=55, required=False)
    placeholder_zipcode = blocks.CharBlock(max_length=55, required=False)
    button_text = blocks.CharBlock(max_length=255, required=False)
    success_message = blocks.CharBlock(max_length=999, required=False)
    form_description = blocks.TextBlock(required=False, help_text='Optional')

    class Meta:
        template = "streams/detail/found_lower_popup.html"
        icon = "snippet"
        label = "FoundLower"


class Reserve(blocks.StructBlock):
    title = blocks.CharBlock(max_length=30, required=False)
    sub_title = blocks.CharBlock(max_length=150, required=False)
    text = blocks.RichTextBlock(required=False)
    button_text = blocks.CharBlock(max_length=30, required=False)

    class Meta:
        template = "streams/detail/reserve_popup.html"
        icon = "snippet"
        label = "Reserve"


class AdditionalMessage(blocks.StructBlock):
    message_text = blocks.TextBlock()

    class Meta:
        template = "streams/detail/additional_message.html"
        icon = "warning"
