from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel

from wagtail.wagtailadmin.edit_handlers import FieldPanel

SHIPPING_METHOD_MODEL_CLASSES = []


def get_default_shipping_method_content_type():
    """
    Returns the content type to use as a default for shipping methods whose content type
    has been deleted.
    """
    return ContentType.objects.get_for_model(ShippingMethod)


class ShippingMethodQueryset(models.QuerySet):
    pass


class BaseShippingMethodManager(models.Manager):
    def get_queryset(self):
        return ShippingMethodQueryset(self.model)


ShippingMethodManager = BaseShippingMethodManager.from_queryset(ShippingMethodQueryset)


class ShippingMethodBase(models.base.ModelBase):
    """
    Metaclass for Shipping Method
    """
    def __init__(cls, name, bases, dct):
        super(ShippingMethodBase, cls).__init__(name, bases, dct)

        if not cls._meta.abstract:
            # register this type in the list of page content types
            SHIPPING_METHOD_MODEL_CLASSES.append(cls)


class AbstractShippingMethod(models.Model):
    """
    Abstract superclass for Page. According to Django's inheritance rules, managers set on
    abstract models are inherited by subclasses, but managers set on concrete models that are extended
    via multi-table inheritance are not. We therefore need to attach PageManager to an abstract
    superclass to ensure that it is retained by subclasses of Page.
    """
    objects = ShippingMethodManager()

    class Meta:
        abstract = True


class ShippingMethod(AbstractShippingMethod, ClusterableModel, metaclass=ShippingMethodBase):
    store = models.ForeignKey('wagtailcommerce_stores.Store', related_name='shipping_methods')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_('content type'),
        related_name='shipping_methods',
        on_delete=models.SET(get_default_shipping_method_content_type)
    )

    panels = [
        FieldPanel('store'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            # this model is being newly created
            # rather than retrieved from the db;
            if not self.content_type_id:
                # set content type to correctly represent the model class
                # that this was created as
                self.content_type = ContentType.objects.get_for_model(self)

    def calculate_cost(self, cart, address):
        """
        Return the shipping cost
        """
        raise NotImplementedError

    def generate_shipment(self, order):
        """
        Generate the actual shipment order
        """
        raise NotImplementedError


class Shipment(models.Model):
    shipping_method = models.ForeignKey(ShippingMethod, related_name='shipments')
    tracking_code = models.CharField(_('tracking code'), max_length=255, blank=True)

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    class Meta:
        verbose_name = _('shipment')
        verbose_name_plural = _('shipments')


# TODO: add shipping records
# class ShippingRecord(models.Model):
#     pass
