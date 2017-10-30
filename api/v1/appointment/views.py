from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from entities.appointment.models import Appointment
from libs.authentication import UserAuthentication
from libs.custom_exceptions import InvalidInputDataException, AppointmentDoesNotExistsException
from libs.permission import PatientDoctorPermission, DoctorPermission
from api.v1.serializers import AppointmentSerializer
from libs.utils import get_datetime_from_date_string

User = get_user_model()


class AppointmentView(APIView):
    """
    View for creating and getting appointment.

    **Example requests**:

        GET /appointment/
            - id=1
        POST /appointment/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission,)

    def get(self, request):
        id = request.query_params.get("id", None)
        try:
            appointment = Appointment.objects.get(id=id)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            raise AppointmentDoesNotExistsException()

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentListView(APIView):
    """
    View for getting all appointments.

    **Example requests**:

        GET /appointment/list/

    **filters**:
        - patient_id
        - doctor_id
        - status=1
        - clinic_id=1
        - reason_id=1

        NOTE: No need to give PATIENT/DOCTOR, if you want to get appointments of logged in user
    """

    authentication_classes = (UserAuthentication,)

    def get(self, request):
        if 'patient_id' in request.query_params:
            appointments = Appointment.objects.filter(patient=request.query_params.get('patient_id'))
        elif 'doctor_id' in request.query_params:
            appointments = Appointment.objects.filter(doctor=request.query_params.get('doctor_id'))
        else:
            if request.user.role == User.Role.DOCTOR:
                appointments = request.user.doctor_appointments.all()
            else:
                appointments = request.user.patient_appointments.all()

        if 'start_date' in request.query_params:
            start_datetime = get_datetime_from_date_string(request.query_params.get("start_date"))
            appointments = appointments.filter(start_datetime__gte=start_datetime)

        if 'end_date' in request.query_params:
            end_datetime = get_datetime_from_date_string(request.query_params.get("end_date"))
            appointments = appointments.filter(end_datetime__lte=end_datetime)

        if 'status' in request.query_params:
            statuses = [int(id) for id in request.query_params.get('status').split(',')]
            appointments = appointments.filter(status__in=statuses)

        if 'clinic_id' in request.query_params:
            appointments = appointments.filter(clinic_id=request.query_params.get('clinic_id'))

        if 'reason_id' in request.query_params:
            appointments = appointments.filter(reason_id=request.query_params.get('reason_id'))

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentStatusAPIView(APIView):

    """
    View for updating appointments.

    **Example requests**:

        PUT /appointment/status
            - id=1

    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorPermission,)

    def get_object(self):
        try:
            return Appointment.objects.get(id=self.request.query_params.get('id'))
        except Appointment.DoesNotExist:
            raise AppointmentDoesNotExistsException

    def put(self, request):
        appointment_obj = self.get_object()

        serializer = AppointmentSerializer(
            appointment_obj,
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
