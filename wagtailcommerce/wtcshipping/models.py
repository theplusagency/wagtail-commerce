from django.db import models
from django.utils.translation import ugettext_lazy as _

SHIPPING_MODEL_CLASSES = []


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

    def calculate_cost(self, order, address):
        """
        Return the shipping cost
        """
        raise NotImplementedError

    def generate_shipment(self, order):
        raise NotImplementedError

    class Meta:
        verbose_name = _('shipping method')
        verbose_name_plural = _('shipping methods')


# class ShippingRecord(models.Model):
#     pass
