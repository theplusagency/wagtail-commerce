import graphene

from wagtailcommerce.products.models import Category
from wagtailcommerce.products.object_types import CategoryType


def process_category(category):
    if 'data' in category:
        cat = {
            'id': category['id'],
            'name': category['data']['name'],
            'slug': category['data']['slug'],
            'children': []
        }

        if 'children' in category.keys():
            cat['children'] = [process_category(c) for c in category['children']]

        return CategoryType(**cat)


class CategoriesQuery(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        categories = []

        for category in Category.dump_bulk():
            categories.append(process_category(category))

        return categories
