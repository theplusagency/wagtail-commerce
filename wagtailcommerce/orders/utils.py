from decimal import Decimal

from wagtailcommerce.carts.utils import get_cart_from_request
from wagtailcommerce.orders.models import Order, OrderLine


def create_order(request, shipping_address, billing_address, cart=None):
    if not cart:
        cart = get_cart_from_request(request)

    order = Order.objects.create(
        store=request.store,
        user=request.user,
        shipping_address=shipping_address,
        billing_address=billing_address,
        subtotal=Decimal('0'),
        product_discount=Decimal('0'),
        product_tax=Decimal('0'),
        shipping_cost=Decimal('0'),
        shipping_cost_discount=Decimal('0'),
        shipping_cost_tax=Decimal('0'),
        total=Decimal('0'),
        total_inc_tax=Decimal('0'))

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
