from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel


class Store(models.Model):
    site = models.OneToOneField('wagtailcore.Site', blank=True, null=True,
                                on_delete=models.SET_NULL, related_name="store")

    panels = [
        FieldPanel('site')
    ]

    class Meta:
        verbose_name = _("store")
        verbose_name_plural = _("stores")
