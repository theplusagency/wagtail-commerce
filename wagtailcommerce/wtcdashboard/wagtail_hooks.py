from wagtailcommerce.wtcstores.models import Store
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register


class StoreAdmin(ModelAdmin):
    model = Store
    menu_icon = 'date'
    menu_order = 100
    list_display = ('site', )


class WagtailCommerceGroup(ModelAdminGroup):
    menu_label = 'Commerce'
    menu_icon = 'fa-shopping-cart'
    menu_order = 500
    items = [StoreAdmin]

modeladmin_register(WagtailCommerceGroup)
