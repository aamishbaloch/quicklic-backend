from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class City(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class Clinic(models.Model):
    code = models.CharField(_('code'), max_length=6, db_index=True, unique=True)
    name = models.CharField(_('name'), max_length=255, db_index=True)
    phone = models.CharField(_('phone'), max_length=255)
    email = models.EmailField(_('email'), blank=True, null=True)
    website = models.URLField(_('website'), blank=True, null=True)
    location = models.CharField(_('location'), max_length=255)
    city = models.ForeignKey(City, related_name="city")
    country = models.ForeignKey(Country, related_name="country")
    image = models.ImageField(upload_to='uploads/clinics/')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


