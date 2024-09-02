from .models import CheckoutPage, CheckoutTnxPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(CheckoutPage)
class CheckoutPageTS(TranslationOptions):
    fields = ("content",)


@register(CheckoutTnxPage)
class CheckoutPageTS(TranslationOptions):
    fields = ("content",)
