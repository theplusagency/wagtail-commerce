from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import pgettext_lazy, ugettext_lazy as _

from wagtailcommerce.promotions.models import Coupon


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

    def replaced(self):
        """
        Return 'REPLACED' carts.
        """
        return self.filter(status=Cart.REPLACED)

    def paid(self):
        """
        Return 'PAID' carts.
        """
        return self.filter(status=Cart.PAID)


class Cart(models.Model):
    OPEN = 'open'
    CANCELED = 'canceled'  # No longer relevant
    AWAITING_PAYMENT = 'awaiting_payment'
    PAID = 'paid'  # Purchased cart
    REPLACED = 'replaced'  # Superseeded by another cart

    STATUS_CHOICES = (
        (OPEN, pgettext_lazy('Cart status', 'Open')),
        (REPLACED, pgettext_lazy('Cart status', 'Replaced')),
        (AWAITING_PAYMENT, pgettext_lazy('Cart status', 'Awaiting payment')),
        (PAID, pgettext_lazy('Cart status', 'Paid')),
        (CANCELED, pgettext_lazy('Cart status', 'Canceled')),
    )

    store = models.ForeignKey('wagtailcommerce_stores.Store', related_name='carts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='carts',
                             on_delete=models.CASCADE, verbose_name=_('user'))
    status = models.CharField(_('status'), max_length=128, default=OPEN, choices=STATUS_CHOICES)

    token = models.UUIDField(_('token'), db_index=True, default=uuid4, editable=False)

    coupon = models.ForeignKey('wagtailcommerce_promotions.Coupon', null=True, blank=True,
                               on_delete=models.SET_NULL)

    updated = models.DateTimeField(_('updated on'), auto_now=True)
    created = models.DateTimeField(_('created on'), auto_now_add=True)

    objects = CartQueryset.as_manager()

    def __str__(self):
        return "{}".format(self.pk)

    def get_subtotal(self):
        subtotal = Decimal('0')

        for l in self.lines.all():
            subtotal += l.variant.product.price * Decimal(l.quantity)

        return subtotal

    def get_total(self):
        return self.get_subtotal() - self.get_discount()

    def get_discount(self):
        if self.coupon:
            if self.coupon.coupon_type == Coupon.ORDER_TOTAL and self.coupon.coupon_mode == Coupon.COUPON_MODE_PERCENTAGE:
                subtotal = self.get_subtotal()
                return subtotal * (self.coupon.coupon_amount / 100)

        return Decimal('0')

    def get_item_count(self):
        q = 0

        for line in self.lines.all():
            q += line.quantity

        return q

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartLine(models.Model):
    cart = models.ForeignKey(Cart, related_name='lines')
    variant = models.ForeignKey('wagtailcommerce_products.ProductVariant', verbose_name=_('product'), related_name='+')
    quantity = models.PositiveIntegerField(_('quantity'))

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    def get_image(self):
        """
        Filter image sets and obtain cart line's variant's related image set.

        Returns the first image of the set.
        """
        filtering_fields = self.variant.product.specific.image_set_filtering_fields

        image_sets = self.variant.product.image_sets.all()

        for field in filtering_fields:
            # Filter image sets by generic foreign key, value comes from field on variant
            filtering_object = getattr(self.variant.specific, field)
            image_sets = image_sets.filter(
                content_type=ContentType.objects.get_for_model(filtering_object),
                object_id=filtering_object.pk
            )

        return image_sets[0].images.first().image

    def has_stock(self):
        return True if self.variant and self.variant.stock > 0 else False

    def get_item_price(self):
        return self.variant.product.price

    def get_item_discount(self):
        if self.cart.coupon:
            if self.cart.coupon.coupon_type == Coupon.ORDER_TOTAL and self.cart.coupon.coupon_mode == Coupon.COUPON_MODE_PERCENTAGE:
                return self.get_item_price() * (self.cart.coupon.coupon_amount / 100)

        return Decimal('0')

    def get_item_price_with_discount(self):
        return self.get_item_price() - self.get_item_discount()

    def get_total(self):
        return self.get_item_price_with_discount() * self.quantity

    class Meta:
        verbose_name = _('cart line')
        verbose_name_plural = _('cart lines')
        ordering = ('created', )
