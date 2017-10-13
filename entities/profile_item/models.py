from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from entities.clinic.models import Country, Clinic, City

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
    country = models.ForeignKey(Country, related_name="doctor_country")
    city = models.ForeignKey(City, related_name="doctor_city")
    clinic = models.ManyToManyField(Clinic, related_name="doctor_clinics")
    services = models.ManyToManyField(Service, related_name="doctor_services")
    specialization = models.ForeignKey(Specialization, related_name="doctor_specialization")
    degree = models.CharField(_('degree'), max_length=50, db_index=True)

    def __str__(self):
        return "{} {}".format(self.doctor.first_name, self.doctor.last_name)

    class Meta:
        verbose_name = _('Doctor Profile')
        verbose_name_plural = _('Doctor Profiles')


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
