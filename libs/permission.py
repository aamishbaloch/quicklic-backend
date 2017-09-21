from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class UserAccessPermission(permissions.BasePermission):
    message = 'No permission for accessing this view.'

    def has_permission(self, request, view):
        return request.user.is_active


class PatientAccessPermission(UserAccessPermission):

    def has_permission(self, request, view):
        return super(PatientAccessPermission, self).has_permission(request, view) and request.user.role == User.Role.PATIENT
