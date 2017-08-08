from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(_('name'), max_length=128)
    slug = models.SlugField(_('slug'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
        verbose_name=_('parent'))

    objects = models.Manager()
    tree = TreeManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class AbstractProduct(models.Model):
    name = models.CharField(_('name'), max_length=150)
    active = models.BooleanField(_('active'))
    available_on = models.DateTimeField(_('available on'), blank=True, null=True)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), related_name='products')

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _('product')
        verbose_name_plural = _('products')


class AbstractProductVariant(models.Model):
    sku = models.CharField(_('SKU'), max_length=32, unique=True)
    name = models.CharField(pgettext_lazy('Product variant field', 'variant name'), max_length=100, blank=True)
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2)
    attributes = HStoreField(
        pgettext_lazy('Product variant field', 'attributes'), default={})
    images = models.ManyToManyField(
        'ProductImage', through='VariantImage',
        verbose_name=pgettext_lazy('Product variant field', 'images'))

    class Meta:
        verbose_name = _('product variant')
        verbose_name_plural = _('product variants')


class Product(AbstractProduct):
    pass


class ProductVariant(AbstractProductVariant):
    product = models.ForeignKey(Product, related_name='variants')
