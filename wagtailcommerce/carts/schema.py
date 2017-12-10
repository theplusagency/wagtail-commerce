import graphene
from wagtailcommerce.carts.object_types import CartType, CartLineType


class CartQuery(graphene.ObjectType):
    cart = graphene.Field(CartType)
    lines = graphene.List(CartLineType)

    def resolve_products(self, info):
        from wagtailcommerce.carts.models import Cart

        return Cart.objects.latest('pk')

    def resolve_cart(self, info, **kwargs):
        from wagtailcommerce.carts.utils import get_cart_from_request

        return get_cart_from_request(info.context)

    def resolve_lines(self, info, **kwargs):
        from wagtailcommerce.carts.utils import get_cart_from_request
        cart = get_cart_from_request(info.context)
        return cart.lines.all()
