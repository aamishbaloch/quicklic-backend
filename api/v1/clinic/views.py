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
            - code=12123424
    """

    authentication_classes = (UserAuthentication,)

    def get(self, request):
        if 'id' in request.query_params:
            clinic = Clinic.objects.filter(id=request.query_params.get("id")).first()

        elif 'code' in request.query_params:
            clinic = Clinic.objects.filter(code=request.query_params.get("code")).first()

        if clinic:
            serializer = ClinicSerializer(clinic, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise ClinicDoesNotExistsException