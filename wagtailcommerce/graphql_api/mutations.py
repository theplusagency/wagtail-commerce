import graphene

from wagtailcommerce.graphql_api.object_types import CartLineNode


class AddToCart(graphene.Mutation):
    class Arguments:
        variant_id = graphene.Int()

    ok = graphene.Boolean()
    cart_line = graphene.Field(lambda: CartLineNode)

    def mutate(self, info, variant_id, *args):
        from wagtailcommerce.carts.utils import add_to_cart
        from wagtailcommerce.products.models import ProductVariant

        try:
            variant = ProductVariant.objects.get(pk=variant_id, product__store=info.context.store)

            if variant.stock < 1:
                print('nostock')
            else:
                cart_line = add_to_cart(info.context, variant)
                print('added')
                print(cart_line.pk)
                return AddToCart(ok=True, cart_line=CartLineNode(variant_id=variant.pk, quantity=cart_line.quantity))

        except ProductVariant.DoesNotExist:
            print('doesnot')

        ok = True
        cart_line_object_type = CartLineNode(
            variant_id=3,
            quantity=2
        )
        return AddToCart(ok=ok, cart_line=cart_line_object_type)
