from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from wagtailcommerce.products.models import Category


class CategoryAdmin(TreeAdmin):
    fields = ('store', 'name', 'slug', '_position', '_ref_node_id',)
    form = movenodeform_factory(Category)
    prepopulated_fields = {
        'slug': ('name', )
    }


admin.site.register(Category, CategoryAdmin)
