from decimal import Decimal

from django.conf import settings

from django.db import models
from django.utils.translation import pgettext_lazy, ugettext_lazy as _


class Cart(models.Model):
    OPEN = 'open'
    LOCKED = 'locked' # Can't be modified. Cloned and locked prior to payment.
    CANCELED = 'canceled' # No longer relevant

    STATUS_CHOICES = (
        (OPEN, pgettext_lazy('Cart status', 'Open')),
        (LOCKED, pgettext_lazy('Cart status', 'Locked')),
        (CANCELED, pgettext_lazy('Cart status', 'Canceled')),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='carts',
                                 on_delete=models.CASCADE, verbose_name=_('customer'))
    status = models.CharField(_('status'), max_length=128, default=OPEN, choices=STATUS_CHOICES)

    updated = models.DateTimeField(_('updated on'), auto_now=True)
    created = models.DateTimeField(_('created on'), auto_now_add=True)

    def __str__(self):
        return "{}".format(self.pk)

    def get_total(self):
        total = Decimal('0')
        for l in self.cart_lines.all:
            total += l.product.price + Decimal(l.quantity)
        return total

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartLine(models.Model):
    variant = models.ForeignKey('wtcproducts.ProductVariant', verbose_name=_('product'), related_name='+')
    quantity = models.PositiveIntegerField(_('quantity'))

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    class Meta:
        verbose_name = _('cart line')
        verbose_name_plural = _('cart lines')
