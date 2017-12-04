import graphene

from .mutations import AddToCart

default_app_config = 'wagtailcommerce.graphql_api.apps.GraphQLAPIAppConfig'


class WagtailCommerceMutations(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
