from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView

from entities.appointment.models import Appointment, Visit
from libs.authentication import UserAuthentication
from libs.permission import (
    PatientDoctorPermission,
    DoctorPermission,
    PKAppointmentOwnerPermission,
    AppointmentOwnerPermission, AppointmentVisitPermission)
from api.v1.serializers import AppointmentSerializer, VisitSerializer
from libs.utils import get_datetime_from_date_string

User = get_user_model()


class AppointmentView(ListCreateAPIView):
    """
    View for creating appointment and listing all.

    **Example requests**:
        GET /appointment/
        POST /appointment/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)
    serializer_class = AppointmentSerializer

    def post(self, request, *args, **kwargs):
        return super(AppointmentView, self).post(request, *args, **kwargs)

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            start_datetime = get_datetime_from_date_string(start_date)
            return Appointment.objects.filter(start_datetime__gte=start_datetime).order_by('start_datetime')
        return Appointment.objects.all().order_by('start_datetime')


class AppointmentDetailView(RetrieveUpdateAPIView):
    """
    View for getting and updating appointment.

    **Example requests**:
        GET /appointment/{id}
        PUT /appointment/{id}
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()


class AppointmentVisitView(CreateAPIView):
    """
    View for creating visit against appointment.

    **Example requests**:
        POST /appointment/{id}/visit/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorPermission, PKAppointmentOwnerPermission)
    serializer_class = VisitSerializer


class AppointmentVisitUpdateView(RetrieveUpdateAPIView):
    """
    View for updating visit against appointment.

    **Example requests**:
        POST /appointment/{id}/visit/{id}
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorPermission, AppointmentOwnerPermission, AppointmentVisitPermission)
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
