from .models import ErrorPage404
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(ErrorPage404)
class HomePageTR(TranslationOptions):
    fields = (
        "title",
        "sub_title",
        "textarea",
        "button_text",
      )
