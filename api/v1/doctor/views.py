from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from libs.authentication import UserAuthentication
from libs.custom_exceptions import InvalidInputDataException
from libs.permission import DoctorPermission
from libs.utils import str2bool
from api.v1.serializers import DoctorSerializer, DoctorUpdateSerializer, ClinicSerializer

User = get_user_model()


class DoctorView(APIView):
    """
    View for creating and getting doctor.

    **Example requests**:

        GET /doctor/
        POST /doctor/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorPermission,)

    def get(self, request):
        serializer = DoctorSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DoctorUpdateSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            serializer = DoctorSerializer(doctor, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidInputDataException(str(serializer.errors))


class DoctorListView(APIView):
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
        - query=aamish
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

        if 'query' in request.query_params:
            doctors = doctors.filter(Q(first_name__icontains=request.query_params.get('query')) | Q(last_name__icontains=request.query_params.get('query')))

        doctors = doctors.filter(is_active=str2bool(request.query_params.get('active', 'true'))).select_related('doctor_profile')

        serializer = DoctorSerializer(doctors, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorClinicView(APIView):
    """
    View for getting doctor's clinics.

    **Example requests**:

        GET /doctor/clinic/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorPermission,)

    def get(self, request):
        clinics = request.user.doctor_profile.clinic.filter(is_active=True)
        serializer = ClinicSerializer(clinics, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
