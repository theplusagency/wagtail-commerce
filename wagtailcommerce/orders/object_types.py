import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.orders.models import Order


class OrderObjectType(DjangoObjectType):
    display_day_placed = graphene.Field(graphene.String)
    display_time_placed = graphene.Field(graphene.String)
    product_count = graphene.Field(graphene.Int)

    def resolve_display_day_placed(self, info, **kwargs):
        return self.date_placed.strftime('%d/%m/%Y')

    def resolve_display_time_placed(self, info, **kwargs):
        return self.date_placed.strftime('%H:%M')

    def resolve_product_count(self, info, **kwargs):
        return self.product_count()

    class Meta:
        model = Order
