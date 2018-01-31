import graphene
import mercadopago

from django.conf import settings
from django.core.urlresolvers import reverse

from wagtailcommerce.addresses.models import Address
from wagtailcommerce.orders.object_types import OrderObjectType
from wagtailcommerce.orders.utils import create_order

from mercadopago_payments.models import MercadoPagoBasicPayment, MercadoPagoBasicIPN


class PlaceOrder(graphene.Mutation):
    class Arguments:
        shipping_address_pk = graphene.String()
        billing_address_pk = graphene.String()

    payment_redirect_url = graphene.String()
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

        accessToken = mp.get_access_token()

        root_url = info.context.site.root_url

        preference = {
            'items': [
                {
                    'id': line.product_variant.product.identifier,
                    'title': line.product_variant.product.name,
                    'currency_id': 'ARS',
                    'picture_url': '{}{}'.format(root_url, line.product_thumbnail.url),
                    'category_id': 'fashion',
                    'quantity': line.quantity,
                    'unit_price': float(line.item_price_with_discount),
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
            'auto_return': 'approved',
            'external_reference': order.identifier,
        }

        preference_result = mp.create_preference(preference)

        MercadoPagoBasicPayment.objects.create(
            order=order,
            preference_sent_data=preference,
            preference_response_data=preference_result,
            preference_id=preference_result['response']['id']
        )

        payment_redirect_url = preference_result['response']['init_point']

        return PlaceOrder(success=True, order=order, payment_redirect_url=payment_redirect_url)
