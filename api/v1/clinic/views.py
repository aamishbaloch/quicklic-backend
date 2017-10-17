from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from entities.clinic.models import Clinic
from libs.authentication import UserAuthentication
from libs.custom_exceptions import ClinicDoesNotExistsException, ClinicAlreadyAddedException
from api.v1.serializers import ClinicSerializer
from libs.permission import PatientPermission

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
            serializer = ClinicSerializer(clinic, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Clinic.DoesNotExist:
            raise ClinicDoesNotExistsException()


class AddPatientToClinicView(APIView):
    """
    View for adding patient into clinic through code.

    **Example requests**:

        POST /clinic/add/patient/
            - code=CODE123
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientPermission,)

    def post(self, request):
        code = request.data.get("code", None)
        try:
            clinic = Clinic.objects.get(code=code)
            if request.user.patient_profile.clinic.filter(code=code).count() <= 0:
                request.user.patient_profile.clinic.add(clinic)
                return Response({}, status=status.HTTP_200_OK)
            else:
                raise ClinicAlreadyAddedException()
        except Clinic.DoesNotExist:
            raise ClinicDoesNotExistsException()
