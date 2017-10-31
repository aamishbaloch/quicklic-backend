from django.contrib.auth import get_user_model
from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from entities.clinic.models import Country, Clinic, City
from libs.utils import get_time_from_string

User = get_user_model()


class Specialization(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    doctor = models.OneToOneField(User, related_name="doctor_profile")
    country = models.ForeignKey(Country, related_name="doctor_country", blank=True, null=True)
    city = models.ForeignKey(City, related_name="doctor_city", blank=True, null=True)
    clinic = models.ManyToManyField(Clinic, related_name="doctor_clinics")
    services = models.ManyToManyField(Service, related_name="doctor_services")
    specialization = models.ForeignKey(Specialization, related_name="doctor_specialization", blank=True, null=True)
    degree = models.CharField(_('degree'), max_length=50, blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.doctor.first_name, self.doctor.last_name)

    class Meta:
        verbose_name = _('Doctor Profile')
        verbose_name_plural = _('Doctor Profiles')


class DoctorSetting(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_setting')
    start_time = models.TimeField(db_index=True)
    end_time = models.TimeField(db_index=True)
    weekdays = ArrayField(models.BooleanField(default=True), size=7)

    def __str__(self):
        return "{} {}".format(self.doctor.first_name, self.doctor.last_name)

    @staticmethod
    def create_settings(user):
        start_time = end_time = get_time_from_string("00:00")
        doctor_setting = DoctorSetting(
            doctor=user, start_time=start_time,
            end_time=end_time,
            weekdays=[True, True, True, True, True, False, False]
        )
        doctor_setting.save()
        return doctor_setting

    def get_weekdays_dict(self):
        weekdays = {
            "Monday": self.weekdays[0],
            "Tuesday": self.weekdays[1],
            "Wednesday": self.weekdays[2],
            "Thursday": self.weekdays[3],
            "Friday": self.weekdays[4],
            "Saturday": self.weekdays[5],
            "Sunday": self.weekdays[6],
        }
        return weekdays


class Occupation(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PatientProfile(models.Model):

    class MaritalStatus:
        MARRIED = 1
        SINGLE = 2

        Choices = (
            (MARRIED, 'MARRIED'),
            (SINGLE, 'SINGLE'),
        )

    patient = models.OneToOneField(User, related_name="patient_profile")
    country = models.ForeignKey(Country, related_name="patient_country", blank=True, null=True)
    city = models.ForeignKey(City, related_name="patient_city", blank=True, null=True)
    clinic = models.ManyToManyField(Clinic, related_name="patient_clinics")
    height = models.FloatField(_('height'), blank=True, null=True)
    weight = models.FloatField(_('weight'), blank=True, null=True)
    occupation = models.ForeignKey(Occupation, related_name="patient_occupation", blank=True, null=True)
    marital_status = models.IntegerField(_('marital status'), choices=MaritalStatus.Choices, blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.patient.first_name, self.patient.last_name)

    class Meta:
        verbose_name = _('Patient Profile')
        verbose_name_plural = _('Patient Profiles')


@receiver(post_save, sender=User)
def user_post_save_callback(sender, instance, **kwargs):
    """
    Save mobile app history after saving the mobile app data.
    """
    user = instance
    if user.role == User.Role.DOCTOR:
        if not hasattr(user, "doctor_profile"):
            doctor_profile = DoctorProfile(doctor=user)
            doctor_profile.save()
        if not hasattr(user, "doctor_setting"):
            DoctorSetting.create_settings(user)
    elif user.role == User.Role.PATIENT:
        if not hasattr(user, "patient_profile"):
            patient_profile = PatientProfile(patient=user)
            patient_profile.save()
