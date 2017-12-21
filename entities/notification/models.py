from django.db import models
from django.utils.translation import ugettext_lazy as _
from entities.clinic.models import Clinic
from entities.person.models import Patient, Doctor, User
from libs.onesignal_sdk import OneSignalSdk


class Notification(models.Model):

    class Message:
        APPOINTMENT_CREATED = "New Appointment {} has been Scheduled."
        APPOINTMENT_CANCELED = "Appointment {} has been Canceled."
        APPOINTMENT_UPDATED = "Appointment {} has been Updated."
        APPOINTMENT_CONFIRMED = "Appointment {} has been Confirmed."
        APPOINTMENT_NOSHOW = "Appointment {} has been Marked as No-Show."

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

    user = models.ForeignKey(User, related_name='notifications')
    patient = models.ForeignKey(Patient, related_name='patient_notifications')
    doctor = models.ForeignKey(Doctor, related_name='doctor_notifications')
    clinic = models.ForeignKey(Clinic, related_name='clinic_notifications')

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    @staticmethod
    def create_notification(user, text, type, patient=None, doctor=None, clinic=None):
        Notification.objects.create(user=user, type=type, text=text, patient=patient, doctor=doctor, clinic=clinic)
        one_signal_sdk = OneSignalSdk()
        one_signal_sdk.create_notification(contents="text", heading="Quicklic", player_ids=[user.device_id])
