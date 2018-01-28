import graphene
from django.utils.translation import ugettext_lazy as _

from wagtailcommerce.addresses.forms import AddressForm
from wagtailcommerce.addresses.models import Address
from wagtailcommerce.addresses.object_types import AddressObjectType, AddressInput
from wagtailcommerce.accounts.object_types import UserObjectType


class EditAddress(graphene.Mutation):
    class Arguments:
        address = AddressInput(required=True)

    success = graphene.Boolean()
    user = graphene.Field(lambda: UserObjectType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, address=None, *args):
        if address.pk:
            try:
                address_instance = Address.objects.filter(user=info.context.user).get(pk=address.pk)
            except Address.DoesNotExist:
                return EditAddress(
                    success=False,
                    errors=[_('Error while editing address. Please reload the page and try again.')]
                )
        else:
            address_instance = Address(user=info.context.user)

        for k, v in address.items():
            setattr(address_instance, k, v)

        address_instance.save()

        return EditAddress(success=True, user=info.context.user)
