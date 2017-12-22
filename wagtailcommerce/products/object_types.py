import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.products.models import Product, ProductVariant


class CategoryType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    slug = graphene.String()
    children = graphene.List('wagtailcommerce.products.object_types.CategoryType')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class ProductVariantType(DjangoObjectType):
    product = graphene.Field(ProductType)

    class Meta:
        model = ProductVariant
