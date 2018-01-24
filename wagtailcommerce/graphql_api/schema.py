import graphene

from wagtailcommerce.accounts.schema import UserQuery
from wagtailcommerce.addresses.mutations import EditAddress
from wagtailcommerce.carts.schema import CartQuery
from wagtailcommerce.carts.mutations import AddToCart
from wagtailcommerce.products.schema import CategoriesQuery
from wagtailcommerce.orders.mutations import PlaceOrder


class WagtailCommerceMutations(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    edit_address = EditAddress.Field()
    place_order = PlaceOrder.Field()


class WagtailCommerceQueries(CategoriesQuery, CartQuery, UserQuery, graphene.ObjectType):
    pass
