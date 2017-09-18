from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from .query import ProductQuerySet, ProductVariantQuerySet

PRODUCT_MODEL_CLASSES = []
PRODUCT_VARIANT_MODEL_CLASSES = []


def get_default_product_content_type():
    """
    Returns the content type to use as a default for pages whose content type
    has been deleted.
    """
    return ContentType.objects.get_for_model(Product)


def get_default_product_variant_content_type():
    """
    Returns the content type to use as a default for pages whose content type
    has been deleted.
    """
    return ContentType.objects.get_for_model(ProductVariant)


# class Category(MPTTModel):
#     name = models.CharField(_('name'), max_length=128)
#     slug = models.SlugField(_('slug'), max_length=50)
#     description = models.TextField(_('description'), blank=True)
#     parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
#         verbose_name=_('parent'))
# 
#     objects = models.Manager()
#     tree = TreeManager()
# 
#     def __str__(self):
#         return self.name
# 
#     class Meta:
#         verbose_name = _('category')
#         verbose_name_plural = _('categories')


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
        app_label = 'wagtailcommerce_products'


class Product(six.with_metaclass(ProductBase, AbstractProduct, ClusterableModel)):
    store = models.ForeignKey('wagtailcommerce_stores.Store', related_name='products')
    name = models.CharField(_('name'), max_length=150)
    active = models.BooleanField(_('active'))
    available_on = models.DateTimeField(_('available on'), blank=True, null=True)
    # categories = models.ManyToManyField(Category, verbose_name=_('categories'), related_name='products')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_('content type'),
        related_name='products',
        on_delete=models.SET(get_default_product_content_type)
    )

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    panels = [
        FieldPanel('store'),
        FieldPanel('name'),
        FieldPanel('active'),
        FieldPanel('available_on'),
    ]

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        if not self.id:
            # this model is being newly created
            # rather than retrieved from the db;
            if not self.content_type_id:
                # set content type to correctly represent the model class
                # that this was created as
                self.content_type = ContentType.objects.get_for_model(self)


class BaseProductVariantManager(models.Manager):
    def get_queryset(self):
        return ProductVariantQuerySet(self.model)

ProductVariantManager = BaseProductVariantManager.from_queryset(ProductQuerySet)


class AbstractProductVariant(models.Model):
    objects = ProductVariantManager()

    class Meta:
        abstract = True
        app_label = 'wagtailcommerce_products'


class ProductVariantBase(models.base.ModelBase):
    """
    Metaclass for Product Variant
    """
    def __init__(cls, name, bases, dct):
        super(ProductVariantBase, cls).__init__(name, bases, dct)

        if not cls._meta.abstract:
            # register this type in the list of product content types
            PRODUCT_VARIANT_MODEL_CLASSES.append(cls)


class ProductVariant(six.with_metaclass(ProductVariantBase, AbstractProductVariant, ClusterableModel)):
    product = ParentalKey(Product, related_name='variants')
    sku = models.CharField(_('SKU'), max_length=32, unique=True)
    name = models.CharField(_('name'), max_length=100, blank=True)
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2)

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_('content type'),
        related_name='product_variants',
        on_delete=models.SET(get_default_product_variant_content_type)
    )

    panels = [
        FieldPanel('product'),
        FieldPanel('sku'),
        FieldPanel('name'),
        FieldPanel('price')
    ]

    def __init__(self, *args, **kwargs):
        super(ProductVariant, self).__init__(*args, **kwargs)
        if not self.id:
            # this model is being newly created
            # rather than retrieved from the db;
            if not self.content_type_id:
                # set content type to correctly represent the model class
                # that this was created as
                self.content_type = ContentType.objects.get_for_model(self)
