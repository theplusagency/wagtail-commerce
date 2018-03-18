from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel


class Coupon(models.Model):
    CATEGORY_TYPE = 'category'
    ORDER_TOTAL = 'order_total'
    PRODUCTS_TYPE = 'products'
    SHIPPING_TYPE = 'shipping'

    COUPON_TYPE_CHOICES = (
        (ORDER_TOTAL, _('Discount on order total')),
        # (CATEGORY_TYPE, _('Products in categories')),
        # (PRODUCTS_TYPE, _('Specific products')),
        # (SHIPPING_TYPE, _('Shipping cost'))
    )

    COUPON_MODE_FIXED = 'fixed'
    COUPON_MODE_PERCENTAGE = 'percentage'

    COUPON_MODE_CHOICES = (
        (COUPON_MODE_FIXED, _('Fixed amount')),
        (COUPON_MODE_PERCENTAGE, _('Percentage')),
    )

    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=40, unique=True, db_index=True)

    coupon_type = models.CharField(_('coupon type'), max_length=20, choices=COUPON_TYPE_CHOICES)
    coupon_mode = models.CharField(_('coupon mode'), max_length=20, choices=COUPON_MODE_CHOICES)
    coupon_amount = models.DecimalField(_('coupon amount'), decimal_places=2, max_digits=12)

    usage_limit = models.PositiveIntegerField(_('usage limit'), null=True, blank=True)
    added_to_cart = models.PositiveIntegerField(_('times added to cart'), default=0, editable=False)
    used = models.PositiveIntegerField(_('times used'), default=0, editable=False)

    auto_assign_to_new_users = models.BooleanField(_('auto assign to new users'))

    active = models.BooleanField(_('active'), default=True)

    valid_from = models.DateTimeField(_('valid from'), blank=True, null=True)
    valid_until = models.DateTimeField(_('valid until'), blank=True, null=True)

    auto_generated = models.BooleanField(_('auto generated'), editable=False, default=False)

    created = models.DateTimeField(_('created on'), auto_now_add=True)
    modified = models.DateTimeField(_('modified on'), auto_now=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('code'),
        ], heading=_('basic information')),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('coupon_type'),
                FieldPanel('coupon_mode'),
            ]),
            FieldRowPanel([
                FieldPanel('coupon_amount'),
            ]),
            FieldRowPanel([
                FieldPanel('usage_limit'),
                FieldPanel('auto_assign_to_new_users'),
            ])
        ], heading=_('characteristics')),
        MultiFieldPanel([
            FieldPanel('active'),
            FieldPanel('valid_from'),
            FieldPanel('valid_until'),
        ], heading=_('validity')),

    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('coupon')
        verbose_name_plural = _('coupons')
