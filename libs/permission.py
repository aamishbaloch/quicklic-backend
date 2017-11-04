from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class UserAccessPermission(permissions.BasePermission):
    message = 'Permission Denied'

    def has_permission(self, request, view):
        return request.user.is_active


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(pk=view.kwargs['id'])
        if request.user == user:
            return True
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


class PatientOwnerPermission(PatientPermission, IsOwner):
    pass


class DoctorOwnerPermission(DoctorPermission, IsOwner):
    pass
