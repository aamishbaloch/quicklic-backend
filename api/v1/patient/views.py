from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from libs.authentication import UserAuthentication
from libs.custom_exceptions import InvalidInputDataException
from libs.permission import PatientPermission
from libs.utils import str2bool
from api.v1.serializers import PatientSerializer, PatientUpdateSerializer, ClinicSerializer

User = get_user_model()


class PatientListView(APIView):
    """
    View for getting all patients.

    **Example requests**:

        GET /patient/list/

    **filters**:
        - active=true: Only active doctors
        - clinic_id=1
        - country_id=1
        - city_id=1
        - occupation_id=1
        - marital_status=2
        - query=aamish
    """

    authentication_classes = (UserAuthentication,)

    def get(self, request):
        patients = User.objects.filter(role=User.Role.PATIENT)

        if 'clinic_id' in request.query_params:
            patients = patients.filter(patient_profile__clinic=request.query_params.get('clinic_id', None))

        if 'country_id' in request.query_params:
            patients = patients.filter(patient_profile__country_id=request.query_params.get('country_id'))

        if 'city_id' in request.query_params:
            patients = patients.filter(patient_profile__city_id=request.query_params.get('city_id'))

        if 'occupation_id' in request.query_params:
            patients = patients.filter(patient_profile__occupation_id=request.query_params.get('occupation_id'))

        if 'marital_status' in request.query_params:
            patients = patients.filter(patient_profile__marital_status=request.query_params.get('marital_status'))

        if 'query' in request.query_params:
            patients = patients.filter(Q(first_name__icontains=request.query_params.get('query')) | Q(last_name__icontains=request.query_params.get('query')))

        patients = patients.filter(is_active=str2bool(request.query_params.get('active', 'true'))).select_related('patient_profile')

        serializer = PatientSerializer(patients, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientView(APIView):
    """
    View for creating and getting patient.

    **Example requests**:

        GET /patient/
        POST /patient/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientPermission,)

    def get(self, request):
        serializer = PatientSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PatientUpdateSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            serializer = PatientSerializer(patient, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidInputDataException(str(serializer.errors))


class PatientClinicView(APIView):
    """
    View for getting patient's clinics.

    **Example requests**:

        GET /patient/clinic/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientPermission,)

    def get(self, request):
        clinics = request.user.patient_profile.clinic.filter(is_active=True)
        serializer = ClinicSerializer(clinics, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
