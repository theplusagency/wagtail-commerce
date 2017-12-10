from decimal import Decimal
from uuid import uuid4

from django.conf import settings

from django.db import models
from django.utils.translation import pgettext_lazy, ugettext_lazy as _


class CartQueryset(models.QuerySet):
    def from_store(self, store):
        """
        Return carts belonging to one specific store.
        """
        return self.filter(store=store)

    def for_user(self, user):
        """
        Return carts belonging to one user.
        """
        return self.filter(user=user)

    def for_token(self, token):
        """
        Return anonymous cart for token
        """
        return self.anonymous().filter(token=token)

    def anonymous(self):
        """
        Return anonymous carts.
        """
        return self.filter(user=None)

    def open(self):
        """
        Return 'OPEN' carts.
        """
        return self.filter(status=Cart.OPEN)

    def canceled(self):
        """
        Return 'CANCELED' carts.
        """
        return self.filter(status=Cart.CANCELED)

    # def for_display(self):
    #     """Annotate the queryset for display purposes.
    #     Prefetches additional data from the database to avoid the n+1 queries
    #     problem.
    #     """
    #     return self.prefetch_related(
    #         'lines__variant__product__categories',
    #         'lines__variant__product__images',
    #         'lines__variant__product__product_class__product_attributes__values',  # noqa
    #         'lines__variant__product__product_class__variant_attributes__values',  # noqa
    #         'lines__variant__stock')


class Cart(models.Model):
    OPEN = 'open'
    LOCKED = 'locked'  # Can't be modified. Cloned and locked prior to payment.
    CANCELED = 'canceled'  # No longer relevant

    STATUS_CHOICES = (
        (OPEN, pgettext_lazy('Cart status', 'Open')),
        (LOCKED, pgettext_lazy('Cart status', 'Locked')),
        (CANCELED, pgettext_lazy('Cart status', 'Canceled')),
    )

    store = models.ForeignKey('wagtailcommerce_stores.store', related_name='carts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='carts',
                             on_delete=models.CASCADE, verbose_name=_('user'))
    status = models.CharField(_('status'), max_length=128, default=OPEN, choices=STATUS_CHOICES)

    token = models.UUIDField(_('token'), db_index=True, default=uuid4, editable=False)

    updated = models.DateTimeField(_('updated on'), auto_now=True)
    created = models.DateTimeField(_('created on'), auto_now_add=True)

    objects = CartQueryset.as_manager()

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
    cart = models.ForeignKey(Cart, related_name='lines')
    variant = models.ForeignKey('wagtailcommerce_products.ProductVariant', verbose_name=_('product'), related_name='+')
    quantity = models.PositiveIntegerField(_('quantity'))

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    class Meta:
        verbose_name = _('cart line')
        verbose_name_plural = _('cart lines')
