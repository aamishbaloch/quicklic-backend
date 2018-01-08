from django.db import models
from django.utils.translation import ugettext_lazy as _

from entities.appointment.models import Appointment
from entities.clinic.models import Clinic
from entities.person.models import Patient, Doctor, User, Moderator
from libs.onesignal_sdk import OneSignalSdk


class Notification(models.Model):

    class Message:
        APPOINTMENT_CREATED = {
            "contents": "{patient} has scheduled a new appointment {appointment_id} with you.",
            "headings": "New appointment {appointment_id} has been scheduled.",
        }
        APPOINTMENT_CANCELED = {
            "contents": "{patient} has canceled an appointment {appointment_id} with you.",
            "headings": "Appointment {appointment_id} has been canceled.",
        }
        APPOINTMENT_UPDATED = {
            "contents": "{patient} has updated an appointment {appointment_id} with you.",
            "headings": "Appointment {appointment_id} has been updated.",
        }
        APPOINTMENT_CONFIRMED = {
            "contents": "{doctor} has confirmed your appointment {appointment_id}.",
            "headings": "Appointment {appointment_id} has been confirmed.",
        }
        APPOINTMENT_NOSHOW = {
            "contents": "{doctor} has marked your appointment {appointment_id} as no show.",
            "headings": "Appointment {appointment_id} has been marked as no show.",
        }
        APPOINTMENT_DISCARD = {
            "contents": "{doctor} has discarded your appointment {appointment_id}.",
            "headings": "Appointment {appointment_id} has been discarded.",
        }

    class Type:
        APPOINTMENT = 1
        ANNOUNCEMENT = 2

        Choices = (
            (APPOINTMENT, 'APPOINTMENT'),
            (ANNOUNCEMENT, 'ANNOUNCEMENT'),
        )

    class UserType:
        DOCTOR = 1
        PATIENT = 2
        ADMIN = 3

        Choices = (
            (DOCTOR, 'DOCTOR'),
            (PATIENT, 'PATIENT'),
            (ADMIN, 'ADMIN'),
        )

    content = models.CharField(_('content'), max_length=255)
    heading = models.CharField(_('heading'), max_length=255)
    type = models.IntegerField(_('type'), db_index=True, choices=Type.Choices, default=Type.ANNOUNCEMENT)
    user_type = models.IntegerField(_('user type'), db_index=True, choices=UserType.Choices, default=UserType.DOCTOR)

    user = models.ForeignKey(User, related_name='notifications')
    patient = models.ForeignKey(Patient, related_name='patient_notifications')
    doctor = models.ForeignKey(Doctor, related_name='doctor_notifications')
    moderator = models.ForeignKey(Moderator, related_name='moderator_notifications', blank=True, null=True)
    clinic = models.ForeignKey(Clinic, related_name='clinic_notifications')
    appointment = models.ForeignKey(Appointment, related_name='notifications', blank=True, null=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

    @staticmethod
    def create_notification(user, user_type, heading, content, type, appointment_id=None, patient=None, doctor=None, clinic=None):
        if type == Notification.Type.APPOINTMENT:
            Notification.objects.create(
                user=user, user_type=user_type, type=type, content=content, heading=heading,
                appointment_id=appointment_id, patient=patient, doctor=doctor, clinic=clinic
            )
            one_signal_sdk = OneSignalSdk()
            one_signal_sdk.create_notification(contents=content, heading=heading, player_ids=[user.device_id])
