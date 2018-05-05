from django.core.paginator import Paginator
import graphene

from wagtailcommerce.products.models import Category, Product
from wagtailcommerce.products.object_types import CategoryType, ProductType


def process_category(category):
    if 'data' in category:
        cat = {
            'id': category['id'],
            'name': category['data']['name'],
            'slug': category['data']['slug'],
        }

        cat = Category(**cat)

        if 'children' in category.keys():
            cat.children = [process_category(c) for c in category['children']]

        return cat


class CategoriesQuery(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        categories = []

        for category in Category.dump_bulk():
            categories.append(process_category(category))

        return categories


class BaseProductSearchResult(graphene.ObjectType):
    num_pages = graphene.Int()


class BaseProductsQuery(graphene.ObjectType):

    def get_products_queryset(self, info, *args, **kwargs):
        products = Product.objects.specific().all().filter(active=True)

        params = kwargs.keys()

        if 'parent_categories' in params and kwargs['parent_categories']:
            products = products.filter(categories__pk__in=kwargs['parent_categories'])

        return products

    @classmethod
    def resolve_product_search(cls, info, *args, **kwargs):
        products = cls.get_products_queryset(info, *args, **kwargs)
        print('here')

        params = kwargs.keys()

        if 'page_number' in params and params['page_number'].isdigit():
            if kwargs['page_size'] and kwargs['page_size'].isdigit():
                page_size = int(kwargs['page_size'])
        else:
            page_number = 1
            page_size = 10

        paginator = Paginator(products, page_size)
        print(paginator.count)
        print(paginator.num_pages)
        print(paginator.object_list)
        return cls.get_search_result_class(cls)(products=paginator.page(1), num_pages=paginator.num_pages)
