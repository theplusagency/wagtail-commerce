import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.products.models import Product, ProductVariant


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class ProductVariantType(DjangoObjectType):
    product = graphene.Field(ProductType)

    class Meta:
        model = ProductVariant
