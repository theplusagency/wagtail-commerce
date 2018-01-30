import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.carts.models import Cart, CartLine
from wagtailcommerce.graphql_api.object_types import WagtailImageType
from wagtailcommerce.products.object_types import ProductVariantType


class CartLineType(DjangoObjectType):
    main_image = graphene.Field(WagtailImageType)
    variant = graphene.Field(ProductVariantType)
    item_price = graphene.Float()
    item_discount = graphene.Float()
    item_price_with_discount = graphene.Float()
    total = graphene.Float()

    def resolve_main_image(self, info, **kwargs):
        return self.get_image()

    def resolve_item_price(self, info, **kwargs):
        return self.get_item_price()

    def resolve_item_discount(self, info, **kwargs):
        return self.get_item_discount()

    def resolve_item_price_with_discount(self, info, **kwargs):
        return self.get_item_price_with_discount()

    def resolve_total(self, info, **kwargs):
        return float(self.get_total())

    class Meta:
        model = CartLine


class CartType(DjangoObjectType):
    discount = graphene.Field(graphene.Float)
    total = graphene.Field(graphene.Float)
    lines = graphene.List(CartLineType)

    def resolve_total(self, info, **kwargs):
        return float(self.get_total())

    def resolve_discount(self, info, **kwargs):
        return float(self.get_discount())

    def resolve_lines(self, info, **kwargs):
        return self.lines.all()

    class Meta:
        model = Cart
