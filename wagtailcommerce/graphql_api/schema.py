from wagtailcommerce.products.schema import Query as ProductsQuery
import graphene

from graphene_django.debug import DjangoDebug


class Query(ProductsQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query)
