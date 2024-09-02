# from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
# from .models import StatePage, InventoryPage, DetailPage, CategoryPage, MyStore
#
#
# class StatePageModelAdmin(ModelAdmin):
#     model = StatePage
#     menu_label = 'State Pages'
#     menu_icon = 'site'
#     menu_order = 100
#     add_to_settings_menu = False
#     exclude_from_explorer = True
#
#
# class InventoryPageModelAdmin(ModelAdmin):
#     model = InventoryPage
#     menu_label = 'Inventory Pages'
#     menu_icon = 'link'
#     menu_order = 200
#     add_to_settings_menu = False
#     exclude_from_explorer = True
#
#
# class DetailPageModelAdmin(ModelAdmin):
#     model = DetailPage
#     menu_label = 'Product Detail Pages'
#     menu_icon = 'link'
#     menu_order = 300
#     add_to_settings_menu = False
#     exclude_from_explorer = True
#
#
# class CategoryPageModelAdmin(ModelAdmin):
#     model = CategoryPage
#     menu_label = 'Category Pages'
#     menu_icon = 'link'
#     menu_order = 400
#     add_to_settings_menu = False
#     exclude_from_explorer = True
#
#
# class StoresGroup(ModelAdminGroup):
#     menu_label = 'Store Pages'
#     menu_icon = 'folder-open-1'
#     menu_order = 200
#     items = (StatePageModelAdmin,
#              InventoryPageModelAdmin,
#              DetailPageModelAdmin,
#              CategoryPageModelAdmin,)
#
#
# modeladmin_register(StoresGroup)
