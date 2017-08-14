from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField


class Address(models.Model):
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last_name'), max_length=255, blank=True)
    company_name = models.CharField(_('company'), max_length=255, blank=True)
    street_address_1 = models.CharField(_('address (line 1)'), max_length=255, blank=True)
    street_address_2 = models.CharField(_('address (line 2)'), max_length=255, blank=True)
    city = models.CharField(_('city / town'), max_length=255, blank=True)
    city_area = models.CharField(_('district / neighborhood'), max_length=255, blank=True)
    country_area = models.CharField(_('state / province'), max_length=255, blank=True)
    country = CountryField(_('country'))
    postal_code = models.CharField(_('postal code'), max_length=64, blank=True)
    phone = models.CharField(_('phone number'), max_length=30, blank=True)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        if self.company_name:
            return '%s - %s' % (self.company_name, self.full_name)
        return self.full_name

    def __repr__(self):
        return (
            'Address (first_name={r}, last_name={r}, company_name={r}, '
            'street_address_1={r}, street_address_2={r}, city={r}, '
            'city_area={r}, country_area={r}, country={r}, '
            'postal_code={r}, phone={r})'.format(
                self.first_name, self.last_name, self.company_name,
                self.street_address_1, self.street_address_2, self.city,
                self.city_area, self.country_area, self.country,
                self.postal_code, self.phone))

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
