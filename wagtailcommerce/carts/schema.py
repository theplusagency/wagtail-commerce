import graphene
from wagtailcommerce.carts.object_types import CartType, CartLineType


class CartQuery(graphene.ObjectType):
    cart = graphene.Field(CartType)

    def resolve_cart(self, info, **kwargs):
        from wagtailcommerce.carts.utils import get_cart_from_request

        return get_cart_from_request(info.context)
