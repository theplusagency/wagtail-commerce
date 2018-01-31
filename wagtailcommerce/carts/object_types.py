import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.carts.models import Cart, CartLine
from wagtailcommerce.graphql_api.object_types import WagtailImageType
from wagtailcommerce.products.object_types import ProductVariantType
from products.object_types import PeakShoeVariantType


class CartLineType(DjangoObjectType):
    main_image = graphene.Field(WagtailImageType)
    variant = graphene.Field(PeakShoeVariantType)
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

    def resolve_variant(self, info, **kwargs):
        return self.variant.specific

    class Meta:
        model = CartLine


class CartType(DjangoObjectType):
    discount = graphene.Field(graphene.Float)
    total = graphene.Field(graphene.Float)
    lines = graphene.List(CartLineType)
    item_count = graphene.Int()

    def resolve_total(self, info, **kwargs):
        return float(self.get_total())

    def resolve_discount(self, info, **kwargs):
        return float(self.get_discount())

    def resolve_lines(self, info, **kwargs):
        return self.lines.all()

    def resolve_item_count(self, info, **kwargs):
        return self.get_item_count()

    class Meta:
        model = Cart
