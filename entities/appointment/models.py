from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from entities.clinic.models import Clinic
from entities.person.models import Patient, Doctor
from entities.resources.models import AppointmentReason

User = get_user_model()


class Appointment(models.Model):

    class Status:
        CONFIRM = 1
        PENDING = 2
        NOSHOW = 3
        CANCEL = 4
        DISCARD = 5
        DONE = 6

        Choices = (
            (CONFIRM, 'CONFIRM'),
            (PENDING, 'PENDING'),
            (NOSHOW, 'NOSHOW'),
            (CANCEL, 'CANCEL'),
            (DISCARD, 'DISCARD'),
            (DONE, 'DONE'),
        )

    qid = models.CharField(_('qid'), max_length=255, db_index=True, unique=True)

    patient = models.ForeignKey(Patient, related_name='appointments')
    doctor = models.ForeignKey(Doctor, related_name='appointments')
    clinic = models.ForeignKey(Clinic, related_name='appointments')

    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(db_index=True)

    reason = models.ForeignKey(AppointmentReason, related_name="appointments")
    status = models.IntegerField(_('status'), db_index=True, choices=Status.Choices, default=Status.PENDING)
    notes = models.TextField(_('notes'), blank=True, null=True)

    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qid


class Visit(models.Model):
    appointment = models.OneToOneField(Appointment, related_name='visit')
    followup_required = models.BooleanField(default=False)
    followup_date = models.DateField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    patient = models.ForeignKey(Patient, related_name='visits')
    doctor = models.ForeignKey(Doctor, related_name='visits')
    clinic = models.ForeignKey(Clinic, related_name='visits')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.appointment.qid
