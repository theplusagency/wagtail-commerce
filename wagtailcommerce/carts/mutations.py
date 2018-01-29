import graphene
from django.utils.translation import ugettext_lazy as _

from wagtailcommerce.carts.utils import get_cart_from_request
from wagtailcommerce.carts.exceptions import CartException
from wagtailcommerce.carts.object_types import CartType, CartLineType


class ModifyCartLine(graphene.Mutation):
    class Arguments:
        variant_pk = graphene.String()
        quantity = graphene.Int()

    success = graphene.Boolean()
    cart = graphene.Field(lambda: CartType)
    deleted = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, variant_pk, quantity, *args):
        from wagtailcommerce.carts.utils import modify_cart_line
        from wagtailcommerce.products.models import ProductVariant

        try:
            variant = ProductVariant.objects.get(pk=variant_pk, product__store=info.context.store)

            try:
                cart_line = modify_cart_line(info.context, variant, quantity)
            except CartException:
                return ModifyCartLine(success=False)

            if cart_line is not None:
                return ModifyCartLine(
                    success=True,
                    cart=get_cart_from_request(info.context)
                )
            else:
                return ModifyCartLine(
                    success=True,
                    deleted=True,
                    cart=get_cart_from_request(info.context)
                )

        except ProductVariant.DoesNotExist:
            return ModifyCartLine(success=False, errors=[_('Product variant not found')])


class AddToCart(graphene.Mutation):
    class Arguments:
        variant_pk = graphene.String()

    success = graphene.Boolean()
    cart = graphene.Field(lambda: CartType)
    errors = graphene.List(graphene.String)
    disableVariant = graphene.Boolean()

    def mutate(self, info, variant_pk, *args):
        from wagtailcommerce.carts.utils import add_to_cart
        from wagtailcommerce.products.models import ProductVariant

        try:
            variant = ProductVariant.objects.get(pk=variant_pk, product__store=info.context.store)

            if variant.stock < 1:
                return AddToCart(success=False, errors=[_('No more products available for the selected size')], disableVariant=True)
            else:
                add_to_cart(info.context, variant)

                return AddToCart(
                    success=True,
                    cart=get_cart_from_request(info.context)
                )

        except ProductVariant.DoesNotExist:
            return AddToCart(success=False, errors=[_('Product variant not found')])

        return AddToCart(ok=ok, cart_line=cart_line_object_type)
