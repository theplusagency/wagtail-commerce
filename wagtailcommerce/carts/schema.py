from django.utils.translation import ugettext_lazy as _

import graphene
from wagtailcommerce.addresses.models import Address
from wagtailcommerce.carts.models import Cart
from wagtailcommerce.carts.object_types import CartType, CartTotalsObjectType
from wagtailcommerce.carts.utils import get_cart_from_request
from wagtailcommerce.shipping.exceptions import ShippingCostCalculationException


class CartQuery(graphene.ObjectType):
    cart = graphene.Field(CartType)

    cart_totals = graphene.Field(
        lambda: CartTotalsObjectType,
        address_pk=graphene.String(required=False),
        shipping_method_code=graphene.String(required=False)
    )

    def resolve_cart_totals(self, info, address_pk, shipping_method_code, **kwargs):
        try:
            address = info.context.user.addresses.get(deleted=False, pk=address_pk)
            cart = get_cart_from_request(info.context)

            shipping_cost = cart.get_shipping_cost(address)

            return CartTotalsObjectType(
                shipping_cost=shipping_cost['total'],
                discount=cart.get_discount(),
                total=cart.get_total() + shipping_cost['total']
            )

        except Address.DoesNotExist:
            raise ShippingCostCalculationException(_('Address not found'))

    def resolve_cart(self, info, **kwargs):
        from wagtailcommerce.carts.utils import get_cart_from_request

        return get_cart_from_request(info.context)
