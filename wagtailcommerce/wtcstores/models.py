from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel


class Currency(models.Model):
    name = models.CharField(_("name"), max_length=128)
    code = models.CharField(_("code"), max_length=3, help_text=_("ISO 4217 3 letter code"))
    symbol = models.CharField(_("symbol"), max_length=30, help_text=_("As displayed on frontend"))

    def __str__(self):
        return "{} ({})".format(self.name, self.code)

    class Meta:
        verbose_name = _("currency")
        verbose_name_plural = _("currencies")



class Store(models.Model):
    name = models.CharField(_("name"), max_length=128)
    site = models.OneToOneField('wagtailcore.Site', blank=True, null=True,
                                on_delete=models.SET_NULL, related_name="store")

    # TODO: allow multiple currencies
    currency = models.ForeignKey(Currency, related_name="stores")

    panels = [
        FieldPanel('site')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("store")
        verbose_name_plural = _("stores")
