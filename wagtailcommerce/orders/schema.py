import graphene

from wagtailcommerce.orders.object_types import OrderObjectType


class OrdersQuery(graphene.ObjectType):
    orders = graphene.List(OrderObjectType)

    def resolve_orders(self, info, **kwargs):
        return info.context.user.orders.all()
