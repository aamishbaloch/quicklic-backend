from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from entities.clinic.models import Clinic
from libs.authentication import UserAuthentication
from libs.custom_exceptions import AppointmentDoesNotExistsException
from api.v1.serializers import ClinicSerializer

User = get_user_model()


class ClinicView(APIView):
    """
    View for getting Clinic.

    **Example requests**:

        GET /clinic/
            - id=1
    """

    authentication_classes = (UserAuthentication,)

    def get(self, request):
        id = request.query_params.get("id", None)
        try:
            clinic = Clinic.objects.get(id=id)
            serializer = ClinicSerializer(clinic)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Clinic.DoesNotExist:
            raise AppointmentDoesNotExistsException()
