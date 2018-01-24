from decimal import Decimal

from wagtailcommerce.carts.utils import get_cart_from_request
from wagtailcommerce.orders.models import Order, OrderLine


def create_order(request, shipping_address, billing_address, cart=None):
    if not cart:
        cart = get_cart_from_request(request)

    order_shipping_address = shipping_address
    order_shipping_address.pk = None
    order_shipping_address.user = None
    order_shipping_address.save()

    order_billing_address = billing_address
    order_billing_address.pk = None
    order_shipping_address.user = None
    order_billing_address.save()

    cart_total = cart.get_total()

    order = Order.objects.create(
        store=request.store,
        user=request.user,
        shipping_address=order_shipping_address,
        billing_address=order_billing_address,
        subtotal=cart_total,
        product_discount=Decimal('0'),
        product_tax=Decimal('0'),
        shipping_cost=Decimal('0'),
        shipping_cost_discount=Decimal('0'),
        shipping_cost_tax=Decimal('0'),
        total=cart_total,
        total_inc_tax=cart_total
    )

    order_lines = []

    for line in cart.lines.select_related('variant', 'variant__product').all():
        order_lines.append(OrderLine(
            order=order,
            sku=line.variant.sku,
            product_variant=line.variant,
            quantity=line.quantity,
            line_price=line.variant.product.price,
            product_name=line.variant.product.name,
            product_variant_description=line.variant.__str__(),
        ))

    OrderLine.objects.bulk_create(order_lines)

    return order
