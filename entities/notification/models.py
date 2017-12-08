from django.db import models
from django.utils.translation import ugettext_lazy as _
from entities.clinic.models import Clinic
from entities.person.models import Patient, Doctor


class Notification(models.Model):

    class Type:
        DOCTOR = 1
        PATIENT = 2
        ADMIN = 3
        GENERAL = 4

        Choices = (
            (DOCTOR, 'DOCTOR'),
            (PATIENT, 'PATIENT'),
            (ADMIN, 'ADMIN'),
            (GENERAL, 'GENERAL'),
        )

    text = models.CharField(_('text'), max_length=255)
    type = models.IntegerField(_('type'), db_index=True, choices=Type.Choices, default=Type.GENERAL)

    patient = models.ForeignKey(Patient, related_name='notifications')
    doctor = models.ForeignKey(Doctor, related_name='notifications')
    clinic = models.ForeignKey(Clinic, related_name='notifications')

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
