from django.contrib.auth import get_user_model
from rest_framework import permissions

from entities.appointment.models import Appointment

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
