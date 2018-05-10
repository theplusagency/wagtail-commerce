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

    def get_products_queryset(cls, info, *args, **kwargs):
        products = Product.objects.specific().all().filter(active=True)

        params = kwargs.keys()
        print('querysetahaaaa')
        if 'parent_categories' in params and kwargs['parent_categories']:
            products = products.filter(categories__pk__in=kwargs['parent_categories'])

        return products

    @classmethod
    def resolve_product_search(cls, info, *args, **kwargs):
        products = cls.get_products_queryset(cls, info, *args, **kwargs)
        print('here')

        params = kwargs.keys()
        print(params)
        print(kwargs['page_size'])

        if 'page_number' in params:
            if 'page_size' in params:
                page_size = kwargs['page_size']

            page_number = kwargs['page_number']
        else:
            page_number = 1
            page_size = 10

        print('psize: {}'.format(page_size))
        paginator = Paginator(products, page_size)
        print(page_number)
        print(paginator.count)
        print(paginator.num_pages)
        print(paginator.object_list)
        return cls.get_search_result_class(cls)(products=paginator.page(page_number), num_pages=paginator.num_pages)
