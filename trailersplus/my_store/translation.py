from .models import MyStore, InventoryPage, CategoryPage, DetailPage, StatePage, BannerMessage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(MyStore)
class MyStoreTR(TranslationOptions):
    fields = ("content",)


@register(InventoryPage)
class InventoryPageTR(TranslationOptions):
    fields = ("content",)


@register(CategoryPage)
class CategoryPageTR(TranslationOptions):
    fields = ("content",)


@register(DetailPage)
class DetailPageTR(TranslationOptions):
    fields = ("content",)


@register(StatePage)
class DetailPageTR(TranslationOptions):
    pass


@register(BannerMessage)
class BannerMessageTR(TranslationOptions):
    fields = ("text",)