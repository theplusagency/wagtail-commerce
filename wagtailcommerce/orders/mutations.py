from decimal import Decimal

import graphene
import mercadopago

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from wagtailcommerce.addresses.models import Address
from wagtailcommerce.carts.utils import get_cart_from_request
from wagtailcommerce.orders.object_types import OrderObjectType
from wagtailcommerce.orders.utils import create_order
from wagtailcommerce.promotions.utils import remove_coupon, verify_coupon

from mercadopago_payments.models import MercadoPagoBasicPayment, MercadoPagoBasicIPN


class PlaceOrder(graphene.Mutation):
    class Arguments:
        shipping_address_pk = graphene.String()
        billing_address_pk = graphene.String()

    payment_redirect_url = graphene.String()
    success = graphene.Boolean()
    order = graphene.Field(lambda: OrderObjectType)
    error = graphene.String()

    @transaction.atomic
    def mutate(self, info, shipping_address_pk, billing_address_pk, *args):
        try:
            shipping_address = Address.objects.get(user=info.context.user, pk=shipping_address_pk)
        except Address.DoesNotExist:
            raise Exception

        try:
            billing_address = Address.objects.get(user=info.context.user, pk=billing_address_pk)
        except Address.DoesNotExist:
            raise Exception

        cart = get_cart_from_request(info.context)

        if cart.coupon and not verify_coupon(cart.coupon):
            coupon_code = cart.coupon.code
            remove_coupon(cart)
            return PlaceOrder(error=_('The coupon "{}" you were currently using is no longer valid. It may have expired or reached its maximum uses.'.format(coupon_code)))

        order = create_order(info.context, shipping_address, billing_address)

        mp = mercadopago.MP(settings.MERCADOPAGO_CLIENT_ID, settings.MERCADOPAGO_CLIENT_SECRET)

        mp.get_access_token()

        root_url = info.context.site.root_url

        items = [
            {
                'id': line.product_variant.product.identifier,
                'title': line.product_variant.product.name,
                'currency_id': 'ARS',
                'picture_url': '{}{}'.format(root_url, line.product_thumbnail.url) if line.product_thumbnail else '',
                'category_id': 'fashion',
                'quantity': line.quantity,
                'unit_price': float(line.item_price_with_discount),
            } for line in order.lines.select_related('product_variant', 'product_variant__product').all()
        ]

        if order.shipping_cost_total > Decimal(0):
            items.append({
                'title': 'Envío',
                'category_id': 'others',
                'currency_id': 'ARS',
                'quantity': 1,
                'unit_price': float(order.shipping_cost_total)
            })

        preference = {
            'items': items,
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
