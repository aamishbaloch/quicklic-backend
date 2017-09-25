from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.authentication import UserAuthentication
from libs.permission import UserAccessPermission, PatientAccessPermission
from libs.utils import str2bool
from .serializers import DoctorSerializer

User = get_user_model()


class DoctorView(APIView):
    """
    View for getting all doctors.

    **Example requests**:

        GET /doctor/all/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientAccessPermission,)

    def get(self, request):
        doctors = User.objects.filter(
            role=User.Role.DOCTOR,
            is_active=str2bool(request.query_params.get('active', 'true')))
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorProfileView(APIView):
    """
    View for getting doctor details.

    **Example requests**:

        GET /doctor/profile/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientAccessPermission,)

    def get(self, request, doctor):


        # serializer = DoctorSerializer(doctors, many=True)
        return Response(None, status=status.HTTP_200_OK)