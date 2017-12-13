import graphene

from wagtailcommerce.carts.schema import CartQuery
from wagtailcommerce.carts.mutations import AddToCart
from wagtailcommerce.products.schema import CategoriesQuery


class WagtailCommerceMutations(graphene.ObjectType):
    add_to_cart = AddToCart.Field()


class WagtailCommerceQueries(CartQuery, CategoriesQuery, graphene.ObjectType):
    pass
