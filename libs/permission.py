from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class UserAccessPermission(permissions.BasePermission):
    message = 'Permission Denied'

    def has_permission(self, request, view):
        return request.user.is_active


class PatientPermission(UserAccessPermission):

    def has_permission(self, request, view):
        return super(PatientPermission, self).has_permission(request, view) and request.user.role == User.Role.PATIENT


class DoctorPermission(UserAccessPermission):

    def has_permission(self, request, view):
        return super(DoctorPermission, self).has_permission(request, view) and request.user.role == User.Role.DOCTOR


class PatientDoctorPermission(UserAccessPermission):

    def has_permission(self, request, view):
        return super(PatientDoctorPermission, self).has_permission(request, view) and \
               (request.user.role == User.Role.PATIENT or request.user.role == User.Role.DOCTOR)

