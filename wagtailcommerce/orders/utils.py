import os
from decimal import Decimal

from django.core.files.base import ContentFile
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
    order_billing_address.user = None
    order_billing_address.save()

    cart_total = cart.get_total()
    cart_discount = cart.get_discount()

    order = Order.objects.create(
        store=request.store,
        user=request.user,
        shipping_address=order_shipping_address,
        billing_address=order_billing_address,
        subtotal=cart_total,
        product_discount=cart_discount,
        product_tax=Decimal('0'),
        shipping_cost=Decimal('0'),
        shipping_cost_discount=Decimal('0'),
        shipping_cost_tax=Decimal('0'),
        total=cart_total,
        total_inc_tax=cart_total
    )

    order_lines = []

    for line in cart.lines.select_related('variant', 'variant__product').all():
        order_line = OrderLine(
            order=order,
            sku=line.variant.sku,
            product_variant=line.variant,
            quantity=line.quantity,
            item_price=line.get_item_price(),
            item_discount=line.get_item_discount(),
            item_price_with_discount=line.get_item_price_with_discount(),
            line_total=line.get_total(),
            product_name=line.variant.product.name,
            product_variant_description=line.variant.__str__(),
        )

        image = line.get_image()

        if image:
            source_file = image.get_rendition('max-400x400|format-jpeg|bgcolor-ffffff')
            if source_file.file:
                try:
                    file_content = ContentFile(source_file.file.read())
                    file_name = os.path.split(source_file.file.name)[-1]

                    order_line.product_thumbnail.save(file_name, file_content, save=False)

                    source_file.file.close()
                except FileNotFoundError:
                    pass

        order_lines.append(order_line)

    OrderLine.objects.bulk_create(order_lines)

    return order
