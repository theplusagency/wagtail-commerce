import graphene
import mercadopago

from django.conf import settings
from django.core.urlresolvers import reverse

from wagtailcommerce.addresses.models import Address
from wagtailcommerce.orders.object_types import OrderObjectType
from wagtailcommerce.orders.utils import create_order


class PlaceOrder(graphene.Mutation):
    class Arguments:
        shipping_address_pk = graphene.String()
        billing_address_pk = graphene.String()

    success = graphene.Boolean()
    order = graphene.Field(lambda: OrderObjectType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, shipping_address_pk, billing_address_pk, *args):
        try:
            shipping_address = Address.objects.get(user=info.context.user, pk=shipping_address_pk)
        except Address.DoesNotExist:
            raise Exception

        try:
            billing_address = Address.objects.get(user=info.context.user, pk=billing_address_pk)
        except Address.DoesNotExist:
            raise Exception

        order = create_order(info.context, shipping_address, billing_address)

        mp = mercadopago.MP(settings.MERCADOPAGO_CLIENT_ID, settings.MERCADOPAGO_CLIENT_SECRET)
        mp.sandbox_mode(True)

        accessToken = mp.get_access_token()

        root_url = info.context.site.root_url

        preference = {
            'items': [
                {
                    'id': line.product_variant.product.identifier,
                    'title': line.product_variant.product.name,
                    'currency_id': 'ARS',
                    'picture_url': 'https://www.peaksport.com.ar/media/images/01-E73001A-MONSTER-A-LAKERS-BLACK.max-800x400.png',
                    'category_id': 'fashion',
                    'quantity': line.quantity,
                    'unit_price': float(line.line_price),
                } for line in order.lines.select_related('product_variant', 'product_variant__product').all()
            ],
            'payer': {
                'name': order.user.first_name,
                'surname': order.user.last_name,
                'email': order.user.email,
            },
            'back_urls': {
                'success': '{}{}'.format(root_url, reverse('purchase_summary')),
                'pending': '{}{}?p=1'.format(root_url, reverse('purchase_summary')),
                'failure': '{}{}?e=1'.format(root_url, reverse('checkout')),
            },
            # 'notification_url': '{}{}'.format(root_url, reverse('mercadopago_basic_ipn'))
        }

        print(preference)

        preferenceResult = mp.create_preference(preference)

        print(preferenceResult)
        url = preferenceResult["response"]["sandbox_init_point"]
        print(url)

        return PlaceOrder(success=True, order=order)
