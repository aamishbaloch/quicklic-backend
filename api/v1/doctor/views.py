from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.authentication import UserAuthentication
from libs.utils import str2bool
from api.v1.serializers import DoctorSerializer

User = get_user_model()


class DoctorView(APIView):
    """
    View for getting all doctors.

    **Example requests**:

        GET /doctor/list/

    **filters**:
        - active=true: Only active doctors
        - clinic_id=1
        - country_id=1
        - city_id=1
        - specialization_id=1
        - services_ids=1,2,3
    """

    authentication_classes = (UserAuthentication,)

    def get(self, request):
        doctors = User.objects.filter(role=User.Role.DOCTOR)

        if 'clinic_id' in request.query_params:
            doctors = doctors.filter(doctor_profile__clinic=request.query_params.get('clinic_id', None))

        if 'country_id' in request.query_params:
            doctors = doctors.filter(doctor_profile__country_id=request.query_params.get('country_id'))

        if 'city_id' in request.query_params:
            doctors = doctors.filter(doctor_profile__city_id=request.query_params.get('city_id'))

        if 'specialization_id' in request.query_params:
            doctors = doctors.filter(doctor_profile__specialization_id=request.query_params.get('specialization_id'))

        if 'services_ids' in request.query_params:
            service_ids = [int(id) for id in request.query_params.get('services_ids').split(',')]
            doctors = doctors.filter(doctor_profile__services__in=service_ids)

        doctors = doctors.filter(is_active=str2bool(request.query_params.get('active', 'true'))).select_related('doctor_profile')

        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)