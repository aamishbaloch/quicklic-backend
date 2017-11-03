from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from entities.clinic.models import Clinic
from entities.person.models import Patient
from libs.authentication import UserAuthentication
from libs.custom_exceptions import ClinicDoesNotExistsException, ClinicAlreadyAddedException
from libs.permission import PatientPermission, PatientOwnerPermission
from libs.utils import str2bool
from api.v1.serializers import PatientSerializer, ClinicSerializer

User = get_user_model()


class PatientView(RetrieveUpdateAPIView):
    """
    View for creating and getting patient.

    **Example requests**:

        GET /patient/
        PUT /patient/
        PATCH /patient/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission,)
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class PatientListView(ListAPIView):
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
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def get_queryset(self):
        patients = Patient.objects.all()

        if 'clinic_id' in self.request.query_params:
            patients = patients.filter(clinic=self.request.query_params.get('clinic_id', None))

        if 'country_id' in self.request.query_params:
            patients = patients.filter(country_id=self.request.query_params.get('country_id'))

        if 'city_id' in self.request.query_params:
            patients = patients.filter(city_id=self.request.query_params.get('city_id'))

        if 'occupation_id' in self.request.query_params:
            patients = patients.filter(occupation_id=self.request.query_params.get('occupation_id'))

        if 'marital_status' in self.request.query_params:
            patients = patients.filter(marital_status=self.request.query_params.get('marital_status'))

        if 'query' in self.request.query_params:
            patients = patients.filter(Q(first_name__icontains=self.request.query_params.get('query')) | Q(last_name__icontains=self.request.query_params.get('query')))

        patients = patients.filter(is_active=str2bool(self.request.query_params.get('active', 'true')))

        return patients


class PatientClinicView(APIView):
    """
    View for getting & creating patient's clinics.

    **Example requests**:

        GET /patient/clinic/
        POST /patient/clinic/
            - code=123123
        DELETE /patient/clinic/{id}
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientPermission,)

    def get(self, request):
        clinics = request.user.patient_profile.clinic.filter(is_active=True)
        serializer = ClinicSerializer(clinics, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, clinic_id):
        try:
            clinic = Clinic.objects.get(id=clinic_id)
            if request.user.patient_profile.clinic.filter(id=clinic_id).count() <= 0:
                raise ClinicDoesNotExistsException()
            else:
                request.user.patient_profile.clinic.remove(clinic)
                request.user.patient_profile.save()
                return Response({}, status=status.HTTP_200_OK)
        except Clinic.DoesNotExist:
            raise ClinicDoesNotExistsException()


class PatientDoctorClinicView(APIView):
    """
    View for getting patient's and doctor's common clinics.

    **Example requests**:

        GET /patient/doctor/{doctor_id}/clinic/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientPermission,)

    def get(self, request, doctor_id):
        patient_clinics = request.user.patient_profile.clinic.filter(is_active=True)
        doctor_clinics = Clinic.objects.filter(doctor_clinics__doctor_id=doctor_id)

        common_clinics = []
        for clinic in patient_clinics:
            if clinic in doctor_clinics:
                common_clinics.append(clinic)

        serializer = ClinicSerializer(common_clinics, context={"request": request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
