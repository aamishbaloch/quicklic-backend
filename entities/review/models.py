from django.db import models
from django.utils.translation import ugettext_lazy as _
from entities.clinic.models import Clinic
from entities.person.models import Patient, Doctor


class Review(models.Model):

    class Type:
        DOCTOR = 1
        CLINIC = 2

        Choices = (
            (DOCTOR, 'DOCTOR'),
            (CLINIC, 'CLINIC'),
        )

    rating = models.IntegerField(_('rating'), db_index=True)
    comment = models.TextField(_('comment'), blank=True, null=True)
    type = models.IntegerField(_('type'), choices=Type.Choices)
    created_at = models.DateTimeField(auto_now_add=True)

    creator = models.ForeignKey(Patient, related_name='reviews')
    is_anonymous = models.BooleanField(_('is_anonymous'), default=False)

    doctor = models.ForeignKey(Doctor, related_name='reviews', blank=True, null=True)
    clinic = models.ForeignKey(Clinic, related_name='reviews', blank=True, null=True)

    def __str__(self):
        return str(self.rating)

