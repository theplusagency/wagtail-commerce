from django.conf import settings
import graphene
from graphene_django.types import DjangoObjectType

from django.contrib.auth import get_user_model
from wagtailcommerce.addresses.object_types import AddressObjectType


class UserObjectType(DjangoObjectType):
    addresses = graphene.List(AddressObjectType)

    def resolve_addresses(self, info, **kwargs):
        return self.addresses.filter(deleted=False)

    class Meta:
        model = get_user_model()
