import graphene
from django.utils.translation import ugettext_lazy as _

from wagtailcommerce.carts.object_types import CartLineType


class AddToCart(graphene.Mutation):
    class Arguments:
        variant_pk = graphene.String()

    success = graphene.Boolean()
    cart_line = graphene.Field(lambda: CartLineType)
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
                cart_line = add_to_cart(info.context, variant)
                return AddToCart(
                    success=True,
                    cart_line=cart_line
                )

        except ProductVariant.DoesNotExist:
            return AddToCart(success=False, errors=[_('Product variant not found')])

        return AddToCart(ok=ok, cart_line=cart_line_object_type)
