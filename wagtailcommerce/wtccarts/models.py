from django.db import models
from django.utils.translation import pgettext_lazy, ugettext_lazy as _


class Cart(models.Model):
    OPEN = 'open'
    LOCKED = 'locked' # Can't be modified. Cloned and locked prior to payment.
    PAYMENT_PENDING = 'payment_pending' # Payment has been confirmed only in an insecure way
    PAID = 'paid' # Payment confirmed and effective
    CANCELED = 'canceled' # No longer relevant

    STATUS_CHOICES = (
        (OPEN, pgettext_lazy("Cart status", "Open")),
        (LOCKED, pgettext_lazy("Cart status", "Locked")),
        (PAYMENT_PENDING, pgettext_lazy("Cart status", "Locked")),
        (PAID, pgettext_lazy("Cart status", "Paid")),
        (CANCELED, pgettext_lazy("Cart status", "Canceled")),
    )
    customer = models.ForeignKey(AUTH_USER_MODEL, null=True, related_name='baskets',
                                 on_delete=models.CASCADE, verbose_name=_("customer"))
    status = models.CharField(_("status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)
    created = models.DateTimeField(_("created on"), auto_now_add=True)
