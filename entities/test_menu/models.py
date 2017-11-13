from django.db import models
from django.utils.translation import ugettext_lazy as _
from entities.clinic.models import Clinic


class Test(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    price = models.DecimalField(_('price'), default=0.00, db_index=True, max_digits=10, decimal_places=2)
    description = models.TextField(_('description'), blank=True, null=True)
    sample_required = models.CharField(_('sample'), max_length=255)
    is_common = models.BooleanField(default=False)
    clinic = models.ForeignKey(Clinic, related_name='test')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

