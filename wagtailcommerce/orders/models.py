import shortuuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtailcommerce.orders.signals import order_paid
from wagtailcommerce.promotions.models import Voucher


class Order(models.Model):
    ORDER_STATUS_OPTIONS = (
        ('payment_pending', _('Payment pending')),
        ('paid', _('Paid')),
        ('cancelled', _('Cancelled')),
    )

    identifier = models.CharField(_('identifier'), max_length=8, db_index=True, unique=True)

    status = models.CharField(_('status'), max_length=30, choices=ORDER_STATUS_OPTIONS,
                              default='payment_pending')

    store = models.ForeignKey('wagtailcommerce_stores.Store', related_name='orders', verbose_name=_('store'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', verbose_name=_('user'))
    billing_address = models.ForeignKey('wagtailcommerce_addresses.Address', blank=True, null=True, related_name='orders_by_billing_address')
    shipping_address = models.ForeignKey('wagtailcommerce_addresses.Address', blank=True, null=True, related_name='orders_by_shipping_address')

    # Financial information
    subtotal = models.DecimalField(_('product sub total'), decimal_places=2, max_digits=12)
    product_discount = models.DecimalField(_('product discount'), decimal_places=2, max_digits=12)
    product_tax = models.DecimalField(_('product tax'), decimal_places=2, max_digits=12)
    shipping_cost = models.DecimalField(_('shipping cost'), decimal_places=2, max_digits=12)
    shipping_cost_discount = models.DecimalField(_('shipping cost discount'), decimal_places=2, max_digits=12)
    shipping_cost_tax = models.DecimalField(_('shipping cost tax'), decimal_places=2, max_digits=12)
    total = models.DecimalField(_('order total'), decimal_places=2, max_digits=12)
    total_inc_tax = models.DecimalField(_('order total (inc. tax)'), decimal_places=2, max_digits=12)

    # TODO: multi-currency support. Now a single store can only have one currency.
    # currency = models.ForeignKey('stores.Currency', related_name='orders', verbose_name=_('currency'))

    # Voucher information 
    voucher = models.ForeignKey('wagtailcommerce_promotions.Voucher', verbose_name=_('voucher'), blank=True, null=True, related_name='orders')
    voucher_type = models.CharField(_('voucher type'), max_length=20, choices=Voucher.VOUCHER_TYPE_CHOICES, blank=True)
    voucher_mode = models.CharField(_('voucher mode'), max_length=20, choices=Voucher.VOUCHER_MODE_CHOICES, blank=True)
    voucher_amount = models.DecimalField(_('voucher amount'), decimal_places=2, max_digits=12, blank=True, null=True)
    voucher_code = models.CharField(_('voucher code'), max_length=40, blank=True)

    date_placed = models.DateTimeField(db_index=True, auto_now_add=True)
    date_paid = models.DateTimeField(db_index=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.generate_identifier()

        try:
            previous_state = Order.objects.get(pk=self.pk)

            if previous_state.status == 'payment_pending' and self.status == 'paid':
                # Order has been paid, reduce product stock and trigger event
                order_paid.send(Order, order=self)
        except Order.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def generate_identifier(self):
        shortuuid.set_alphabet('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

        while True:
            uuid = shortuuid.uuid()[:8]
            if not Order.objects.filter(identifier=uuid).exists():
                break

        return uuid

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderLine(models.Model):
    order = models.ForeignKey(Order, related_name='lines')
    sku = models.CharField(_('SKU'), max_length=128)
    product_variant = models.ForeignKey('wagtailcommerce_products.ProductVariant', related_name='lines',
                                        null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    line_price = models.DecimalField(_('line price'), decimal_places=2, max_digits=12)

    voucher_type = models.CharField(_('discount type'), max_length=20, choices=Voucher.VOUCHER_TYPE_CHOICES, blank=True)
    voucher_mode = models.CharField(_('discount mode'), max_length=20, choices=Voucher.VOUCHER_MODE_CHOICES, blank=True)
    voucher_amount = models.DecimalField(_('discount amount'), decimal_places=2, max_digits=12, blank=True, null=True)
    voucher_voucher_code = models.CharField(_('code'), max_length=40, blank=True)

    # Persistent fields. If the linked Product Variant is deleted, the SKU, product name and variant desc. persist.
    product_name = models.CharField(_('product name'), max_length=255)
    product_variant_description = models.CharField(_('product variant description'), max_length=255)

    def __str__(self):
        return "{} ({})".format(self.product_name, self.quantity)

    class Meta:
        verbose_name = _('order line')
        verbose_name_plural = _('order lines')
