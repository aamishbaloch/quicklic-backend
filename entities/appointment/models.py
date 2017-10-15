from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from entities.clinic.models import Clinic

User = get_user_model()


class AppointmentReason(models.Model):
    title = models.CharField(_('name'), max_length=255, db_index=True)

    def __str__(self):
        return self.title


class Appointment(models.Model):

    class Status:
        CONFIRM = 'CONF'
        PENDING = 'PEND'
        NOSHOW = 'NOSW'
        CANCEL = 'CANC'

        Choices = (
            (CONFIRM, 'CONFIRM'),
            (PENDING, 'PENDING'),
            (NOSHOW, 'NOSHOW'),
            (CANCEL, 'CANCEL'),
        )

    qid = models.CharField(_('qid'), max_length=255, db_index=True, unique=True)

    patient = models.ForeignKey(User, related_name='patient')
    doctor = models.ForeignKey(User, related_name='doctor')
    clinic = models.ForeignKey(Clinic, related_name='clinic')

    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(db_index=True)
    duration = models.CharField(max_length=255)

    reason = models.ForeignKey(AppointmentReason, related_name="reason")
    status = models.CharField(_('status'), max_length=4, db_index=True, choices=Status.Choices, blank=True, default=Status.PENDING)

    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.patient.na
