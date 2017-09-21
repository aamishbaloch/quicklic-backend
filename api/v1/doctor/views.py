from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from libs.utils import str2bool
from .serializers import DoctorSerializer


User = get_user_model()


class DoctorView(APIView):
    """
    View for getting doctor details.

    **Example requests**:

        GET /doctor/all/
    """

    def get(self, request):
        doctors = User.objects.filter(
            role=User.Role.DOCTOR,
            is_active=str2bool(request.query_params.get('active', 'true')))
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)