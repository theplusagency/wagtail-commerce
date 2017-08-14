from django.db import models
from django.utils.translation import ugettext_lazy as _

SHIPPING_METHOD_MODEL_CLASSES = []


def get_default_shipping_method_content_type():
    """
    Returns the content type to use as a default for shipping methods whose content type
    has been deleted.
    """
    return ContentType.objects.get_for_model(ShippingMethod)


class ShippingMethodBase(object):
    """
    Metaclass for Shipping Method
    """
    def __init__(cls, name, bases, dct):
        super(ShippingMethodBase, cls).__init__(name, bases, dct)

        if not cls._meta.abstract:
            # register this type in the list of page content types
            SHIPPING_MODEL_CLASSES.append(cls)

        print(SHIPPING_MODEL_CLASSES)


class ShippingMethodQueryset(models.QuerySet):
    pass


class BaseShippingMethodManager(models.Manager):
    def get_queryset(self):
        return ShippingMethodQueryset(self.model)


ShippingMethodManager = BaseShippingMethodManager.from_queryset(ShippingMethodQueryset)


class AbstractShippingMethod(object):
    """
    Abstract superclass for Page. According to Django's inheritance rules, managers set on
    abstract models are inherited by subclasses, but managers set on concrete models that are extended
    via multi-table inheritance are not. We therefore need to attach PageManager to an abstract
    superclass to ensure that it is retained by subclasses of Page.
    """
    objects = ShippingMethodManager()

    class Meta:
        abstract = True


class ShippingMethod(ShippingMethodBase, AbstractShippingMethod, models.Model):
    store = models.ForeignKey('wtcstores.Store', related_name='shipping_methods')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_('content type'),
        related_name='shipping_methods',
        on_delete=models.SET(get_default_shipping_method_content_type)
    )

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

    class Meta:
        verbose_name = _('shipping method')
        verbose_name_plural = _('shipping methods')


class Shipment(models.Model):
    shipping_method = models.ForeignKey(ShippingMethod, related_name='shipments')
    tracking_code = models.CharField(_('tracking code'), max_length=255, blank=True)

    created = models.DateTimeField(_('created on'), auto_now_add=True)

    class Meta:
        verbose_name = _('shipment')
        verbose_name_plural = _('shipments')


# class ShippingRecord(models.Model):
#     pass
