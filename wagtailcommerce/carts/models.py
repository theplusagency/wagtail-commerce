from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


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
        for l in self.lines.all():
            total += l.variant.product.price * Decimal(l.quantity)
        return total

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartLine(models.Model):
    cart = models.ForeignKey(Cart, related_name='lines')
    variant = models.ForeignKey('wagtailcommerce_products.ProductVariant', verbose_name=_('product'), related_name='+')
    quantity = models.PositiveIntegerField(_('quantity'))

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    def get_total(self):
        return self.variant.product.price * self.quantity

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

    class Meta:
        verbose_name = _('cart line')
        verbose_name_plural = _('cart lines')
