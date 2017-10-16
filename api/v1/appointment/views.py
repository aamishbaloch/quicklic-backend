from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from entities.appointment.models import Appointment
from libs.authentication import UserAuthentication
from libs.custom_exceptions import InvalidInputDataException, AppointmentDoesNotExistsException
from libs.permission import PatientDoctorPermission
from api.v1.serializers import AppointmentSerializer

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

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidInputDataException()

    def get(self, request):
        id = request.query_params.get("id", None)
        try:
            appointment = Appointment.objects.get(id=id)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            raise AppointmentDoesNotExistsException()
