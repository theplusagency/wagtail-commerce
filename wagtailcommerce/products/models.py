from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import six
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from treebeard.mp_tree import MP_Node
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtailcommerce.products.query import CategoryQuerySet, ProductQuerySet, ProductVariantQuerySet

CATEGORY_MODEL_CLASSES = []
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


class BaseCategoryManager(models.Manager):
    def get_queryset(self):
        return self._queryset_class(self.model).order_by('path')


CategoryManager = BaseCategoryManager.from_queryset(CategoryQuerySet)


class CategoryBase(models.base.ModelBase):
    """
    Metaclass for Category
    """
    def __init__(cls, name, bases, dct):
        super(CategoryBase, cls).__init__(name, bases, dct)

        if not cls._meta.abstract:
            # register this type in the list of category content types
            CATEGORY_MODEL_CLASSES.append(cls)


class AbstractCategory(MP_Node):
    """
    Abstract superclass for Category. 
    """
    objects = CategoryManager()
    
    class Meta:
        abstract = True


class Category(AbstractCategory, ClusterableModel, metaclass=CategoryBase):
    store = models.ForeignKey('wagtailcommerce_stores.Store', related_name='categories')
    name = models.CharField(_('name'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=50)
    description = models.TextField(_('description'), blank=True)

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
        app_label = 'wagtailcommerce_products'


class Product(AbstractProduct, ClusterableModel, metaclass=ProductBase):
    store = models.ForeignKey('wagtailcommerce_stores.Store', related_name='products')
    name = models.CharField(_('name'), max_length=150)
    slug = models.SlugField(
        verbose_name=_('slug'),
        allow_unicode=True,
        max_length=255,
        help_text=_('The name of the product as it will appear in URLs e.g http://domain.com/store/[product-slug]/'))

    categories = models.ManyToManyField(Category, blank=True, related_name='products')
    single_price = models.BooleanField(_('single price'), default=True, help_text=_('same price for all variants'))
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2, blank=True, null=True)

    active = models.BooleanField(_('active'))
    available_on = models.DateTimeField(_('available on'), blank=True, null=True)

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
        FieldPanel('slug'),
        FieldPanel('active'),
        FieldPanel('available_on'),
        FieldPanel('categories'),
        FieldPanel('single_price'),
        FieldPanel('price'),
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

    @cached_property
    def specific(self):
        """
        Return this product variant in its most specific subclassed form.
        """
        # the ContentType.objects manager keeps a cache, so this should potentially
        # avoid a database lookup over doing self.content_type. I think.
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        model_class = content_type.model_class()
        if model_class is None:
            # Cannot locate a model class for this content type. This might happen
            # if the codebase and database are out of sync (e.g. the model exists
            # on a different git branch and we haven't rolled back migrations before
            # switching branches); if so, the best we can do is return the page
            # unchanged.
            return self
        elif isinstance(self, model_class):
            # self is already the an instance of the most specific class
            return self
        else:
            return content_type.get_object_for_this_type(id=self.id)


class ImageSet(ClusterableModel):
    product = ParentalKey(Product, related_name='image_sets')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    filtering_relation = GenericForeignKey('content_type', 'object_id')

    panels = [
        InlinePanel('images', label=_('images'))
    ]

    def __str__(self):
        return "{}".format(self.filtering_relation)

    class Meta:
        verbose_name = _('image set')
        verbose_name_plural = _('image sets')
        unique_together = ('content_type', 'object_id', )


class Image(Orderable):
    image_set = ParentalKey(ImageSet, related_name='images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('image'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')


class BaseProductVariantManager(models.Manager):
    def get_queryset(self):
        return ProductVariantQuerySet(self.model)


ProductVariantManager = BaseProductVariantManager.from_queryset(ProductVariantQuerySet)


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
    price = models.DecimalField(_('price'), max_digits=12, decimal_places=2, blank=True, null=True)
    active = models.BooleanField(_('active'), default=True)

    stock = models.IntegerField(_('stock'), default=0)

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
        FieldPanel('price'),
        FieldPanel('stock')
    ]

    @cached_property
    def specific(self):
        """
        Return this product variant in its most specific subclassed form.
        """
        # the ContentType.objects manager keeps a cache, so this should potentially
        # avoid a database lookup over doing self.content_type. I think.
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        model_class = content_type.model_class()
        if model_class is None:
            # Cannot locate a model class for this content type. This might happen
            # if the codebase and database are out of sync (e.g. the model exists
            # on a different git branch and we haven't rolled back migrations before
            # switching branches); if so, the best we can do is return the page
            # unchanged.
            return self
        elif isinstance(self, model_class):
            # self is already the an instance of the most specific class
            return self
        else:
            return content_type.get_object_for_this_type(id=self.id)

    def __init__(self, *args, **kwargs):
        super(ProductVariant, self).__init__(*args, **kwargs)
        if not self.id:
            # this model is being newly created
            # rather than retrieved from the db;
            if not self.content_type_id:
                # set content type to correctly represent the model class
                # that this was created as
                self.content_type = ContentType.objects.get_for_model(self)

    def __str__(self):
        return self.specific.__str__()
