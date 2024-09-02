from .models import Menu, MenuItem, MainMenu
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(MainMenu)
class MainMenuTR(TranslationOptions):
    fields = ("menus",)


@register(Menu)
class MenuTR(TranslationOptions):
    fields = ("title",)


@register(MenuItem)
class MenuItemTR(TranslationOptions):
    fields = ("link_title",)
