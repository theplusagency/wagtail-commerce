from django.db import models
from django.utils.translation import ugettext_lazy as _


class Voucher(models.Model):
    CATEGORY_TYPE = 'category'
    PRODUCTS_TYPE = 'products'
    SHIPPING_TYPE = 'shipping'

    VOUCHER_TYPE_CHOICES = (
        (CATEGORY_TYPE, _('Products in categories')),
        (PRODUCTS_TYPE, _('Specific products')),
        (SHIPPING_TYPE, _('Shipping cost'))
    )

    VOUCHER_MODE_FIXED = 'fixed'
    VOUCHER_MODE_PERCENTAGE = 'percentage'

    VOUCHER_MODE_CHOICES = (
        (VOUCHER_MODE_FIXED, _('Fixed amount')),
        (VOUCHER_MODE_PERCENTAGE, _('Percentage'))
    )

    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=40, unique=True, db_index=True)

    voucher_type = models.CharField(_('voucher type'), max_length=20, choices=VOUCHER_TYPE_CHOICES)
    voucher_mode = models.CharField(_('voucher mode'), max_length=20, choices=VOUCHER_MODE_CHOICES)
    voucher_amount = models.DecimalField(_('voucher amount'), decimal_places=2, max_digits=12)

    usage_limit = models.PositiveIntegerField(_('usage limit'), null=True, blank=True)
    used = models.PositiveIntegerField(default=0, editable=False)

    valid_from = models.DateTimeField(_('valid from'), blank=True, null=True)
    valid_until = models.DateTimeField(_('valid from'), blank=True, null=True)

    product_variants = models.ManyToManyField('wtcproducts.ProductVariant', related_name='vouchers')

    auto_generated = models.BooleanField(_('auto generated'), editable=False)
    created = models.DateTimeField(_('created on'), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('voucher')
        verbose_name_plural = _('vouchers')
