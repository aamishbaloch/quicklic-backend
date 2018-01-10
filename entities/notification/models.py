from django.db import models
from django.utils.translation import ugettext_lazy as _

from entities.appointment.models import Appointment
from entities.clinic.models import Clinic
from entities.person.models import Patient, Doctor, User, Moderator
from libs.onesignal_sdk import OneSignalSdk


class Notification(models.Model):

    class Message:
        HEADING = "Quicklic Notification!"

        APPOINTMENT_CREATED = {
            "contents": "{patient} has scheduled a new appointment {appointment_id} with you.",
        }
        APPOINTMENT_CANCELED = {
            "contents": "{patient} has canceled an appointment {appointment_id} with you.",
        }
        APPOINTMENT_UPDATED = {
            "contents": "{patient} has updated an appointment {appointment_id} with you.",
        }
        APPOINTMENT_CONFIRMED = {
            "contents": "{doctor} has confirmed your appointment {appointment_id}.",
        }
        APPOINTMENT_NOSHOW = {
            "contents": "{doctor} has marked your appointment {appointment_id} as no show.",
        }
        APPOINTMENT_DISCARD = {
            "contents": "{doctor} has discarded your appointment {appointment_id}.",
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


    @staticmethod
    def create_batch_notification_for_discard(appointments):
        player_ids = []
        for appointment in appointments:
            Notification.objects.create(
                user=appointment.patient,
                user_type=Notification.UserType.PATIENT,
                type=Notification.Type.APPOINTMENT,
                content=Notification.Message.APPOINTMENT_DISCARD["contents"].format(
                        patient=appointment.doctor.get_full_name(), appointment_id=appointment.qid),
                heading=Notification.Message.HEADING,
                appointment_id=appointment.id,
                patient=appointment.patient,
                doctor=appointment.doctor,
                clinic=appointment.clinic,
            )
            player_ids.append(appointment.patient.device_id)

        one_signal_sdk = OneSignalSdk()
        one_signal_sdk.create_notification(contents="Your appointment has been discarded by the doctor.", heading=Notification.Message.HEADING, player_ids=player_ids)
