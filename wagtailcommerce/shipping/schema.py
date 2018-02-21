import graphene

from wagtailcommerce.products.models import Category
from wagtailcommerce.products.object_types import CategoryType

# from wagtailcommerce.shipping.utils import get_shipping_cost


class ShippingQuery(graphene.ObjectType):
    shipping_cost = graphene.Float(shipping_method_code=graphene.String())

    def resolve_shipping_cost(self, info, shipping_method_code, **kwargs):
        # return float(get_shipping_cost(info))
        return 130
