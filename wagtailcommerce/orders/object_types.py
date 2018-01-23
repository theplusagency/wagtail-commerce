from django.contrib.contenttypes.models import ContentType

import graphene
from graphene_django.types import DjangoObjectType

from wagtailcommerce.orders.models import Order


class OrderObjectType(DjangoObjectType):
    class Meta:
        model = Order
