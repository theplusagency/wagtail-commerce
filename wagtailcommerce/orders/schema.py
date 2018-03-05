import graphene

from wagtailcommerce.orders.object_types import OrderObjectType


class OrdersQuery(graphene.ObjectType):
    orders = graphene.List(OrderObjectType)
    order = graphene.Field(OrderObjectType, pk=graphene.String())

    def resolve_orders(self, info, **kwargs):
        return info.context.user.orders.all()

    def resolve_order(self, info, pk, **kwargs):
        return info.context.user.orders.get(pk=pk)
