from .models import FlatPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(FlatPage)
class HomePageTR(TranslationOptions):
    fields = ("content",)


"""@register(Form)
class FormsTR(TranslationOptions):
    fields = (
        "title",
        "sub_title",
        "submit_button_text",
        "success_message",
        "error_message",
    )"""
