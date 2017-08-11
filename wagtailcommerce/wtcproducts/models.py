from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from wtcproducts.models import ProductQuerySet, ProductVariantQuerySet

PRODUCT_MODEL_CLASSES = []
PRODUCT_VARIANT_MODEL_CLASSES = []


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


class BaseProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model)

ProductManager = BaseProductManager.from_queryset(ProductQuerySet)


class ProductBase(models.base.ModelBase):
    """
    Metaclass for Product
    """
    def __init__(cls, name, bases, dct):
        super(ProductBase, cls).__init__(name, bases, dct)

        if not cls._meta.abstract:
            # register this type in the list of product content types
            PRODUCT_MODEL_CLASSES.append(cls)


class AbstractProduct(models.Model):
    objects = ProductManager()

    class Meta:
        abstract = True


class Product(ProductBase, AbstractProduct):
    name = models.CharField(_('name'), max_length=150)
    active = models.BooleanField(_('active'))
    available_on = models.DateTimeField(_('available on'), blank=True, null=True)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), related_name='products')

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    def __str__(self):
        return self.name


class BaseProductVariantManager(models.Manager):
    def get_queryset(self):
        return ProductVariantQuerySet(self.model)

ProductVariantManager = BaseProductVariantManager.from_queryset(ProductQuerySet)


class AbstractProductVariant(models.Model):
    objects = ProductVariantManager()

    class Meta:
        abstract = True


class ProductVariant(AbstractProductVariant):
    product = models.ForeignKey(Product, related_name='variants')
    sku = models.CharField(_('SKU'), max_length=32, unique=True)
    name = models.CharField(pgettext_lazy('Product variant field', 'variant name'), max_length=100, blank=True)
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2)
    images = models.ManyToManyField(
        'ProductImage', through='VariantImage',
        verbose_name=pgettext_lazy('Product variant field', 'images'))
