from wagtailmenus.models import MainMenuItem

from .models import HomePage, Footer, Header, SearchBar, ErrorPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = ("content",)


@register(MainMenuItem)
class MainMenuTR(TranslationOptions):
    fields = ("link_text",)


@register(Footer)
class FooterTR(TranslationOptions):
    fields = (
        "top_text",
        "location",
        "phone_number",
        "bottom_text",
        "cookie_popup",
        "cookie_popup_button_text",
        "copyright_text",
    )


@register(Header)
class HeaderTR(TranslationOptions):
    fields = (
        "location_icon_text",
        "location_icon_mobile_text",
        "phone_icon_text",
        "cart_title",
        "item_added_text",
        "remove_button",
        "checkout_button",
        "go_to_google_maps"
    )


@register(SearchBar)
class SearchBarTR(TranslationOptions):
    fields = (
        "trailer_type_text",
        "select_store_text",
        "search_button_text",
    )

@register(ErrorPage)
class ErrorPageTR(TranslationOptions):
    fields = (
        "content",
    )
