from django.contrib.auth import get_user_model
from rest_framework import permissions

from entities.appointment.models import Appointment
from entities.notification.models import Notification
from entities.person.models import Doctor

User = get_user_model()


class UserAccessPermission(permissions.BasePermission):
    message = 'Permission Denied'

    def has_permission(self, request, view):
        return request.user.is_active


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = User.objects.get(pk=view.kwargs['pk'])
            if request.user == user:
                return True
            return False
        except User.DoesNotExist:
            return False


class PatientPermission(UserAccessPermission):

    def has_permission(self, request, view):
        return super(PatientPermission, self).has_permission(request, view) and hasattr(request.user, 'patient')


class DoctorPermission(UserAccessPermission):

    def has_permission(self, request, view):
        return super(DoctorPermission, self).has_permission(request, view) and hasattr(request.user, 'doctor')


class PatientDoctorPermission(UserAccessPermission):

    def has_permission(self, request, view):
        return super(PatientDoctorPermission, self).has_permission(request, view) and \
               (hasattr(request.user, 'patient') or hasattr(request.user, 'doctor'))


class PatientOwnerPermission(IsOwner):
    def has_permission(self, request, view):
        return super(PatientOwnerPermission, self).has_permission(request, view) \
               and hasattr(request.user, 'patient')


class DoctorOwnerPermission(IsOwner):
    def has_permission(self, request, view):
        return super(DoctorOwnerPermission, self).has_permission(request, view) \
               and hasattr(request.user, 'doctor')


class AppointmentOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            appointment = Appointment.objects.get(pk=view.kwargs['appointment_id'])
            if request.user.id == appointment.doctor.id or request.user.id == appointment.patient.id:
                return True
            return False
        except Appointment.DoesNotExist:
            return False


class PKAppointmentOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            appointment = Appointment.objects.get(pk=view.kwargs['pk'])
            if request.user.id == appointment.doctor.id or request.user.id == appointment.patient.id:
                return True
            return False
        except Appointment.DoesNotExist:
            return False


class PatientBelongsDoctorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            doctor = Doctor.objects.get(pk=view.kwargs['pk'])
            patient_clinics = request.user.patient.clinic.all().values_list('id', flat=True)
            doctor_clinics = doctor.clinic.all().values_list('id', flat=True)
            if any(patient_clinic in doctor_clinics for patient_clinic in patient_clinics):
                return True
            return False
        except Doctor.DoesNotExist:
            return False


class AppointmentVisitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            appointment = Appointment.objects.get(pk=view.kwargs['appointment_id'])
            if hasattr(appointment, 'visit'):
                if appointment.visit.id == int(view.kwargs['pk']):
                    return True
            return False
        except Appointment.DoesNotExist:
            return False


class PKNotificationOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            notification = Notification.objects.get(pk=view.kwargs['pk'])
            if request.user.id == notification.user.id:
                return True
            return False
        except Notification.DoesNotExist:
            return False