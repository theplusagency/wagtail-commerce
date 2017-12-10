import graphene

from wagtailcommerce.carts.schema import CartQuery
from wagtailcommerce.carts.mutations import AddToCart


class WagtailCommerceMutations(graphene.ObjectType):
    add_to_cart = AddToCart.Field()


class WagtailCommerceQueries(CartQuery, graphene.ObjectType):
    pass
