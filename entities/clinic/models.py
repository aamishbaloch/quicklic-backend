from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Clinic(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    phone = models.CharField(_('phone'), max_length=255)
    location = models.CharField(_('location'), max_length=255)
    city = models.ForeignKey(City, related_name="city")
    country = models.ForeignKey(Country, related_name="coutry")
    image = models.ImageField(upload_to='uploads/clinics/')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


