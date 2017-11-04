from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.db.models import Q
from entities.clinic.models import Clinic
from entities.person.models import Patient, Doctor
from libs.authentication import UserAuthentication
from libs.custom_exceptions import ClinicDoesNotExistsException, ClinicAlreadyAddedException
from libs.permission import PatientOwnerPermission
from libs.utils import str2bool
from api.v1.serializers import PatientSerializer, ClinicSerializer


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


class PatientClinicView(ListAPIView):
    """
    View for getting & creating patient's clinics.

    **Example requests**:

        GET /patient/{id}/clinic/
        POST /patient/{id}/clinic/
            - code="123123"
        DELETE /patient/{id}/clinic/{id}
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission,)
    serializer_class = ClinicSerializer

    def get_queryset(self):
        return self.request.user.clinic.all().order_by('id')

    def post(self, request, pk):
        code = request.data.get("code", None)
        try:
            clinic = Clinic.objects.get(code=code)
            if request.user.clinic.filter(code=code).count() <= 0:
                request.user.clinic.add(clinic)
                return Response({}, status=status.HTTP_200_OK)
            else:
                raise ClinicAlreadyAddedException()
        except Clinic.DoesNotExist:
            raise ClinicDoesNotExistsException()

    def delete(self, request, pk, clinic_id):
        try:
            clinic = Clinic.objects.get(id=clinic_id)
            if request.user.clinic.filter(id=clinic_id).count() <= 0:
                raise ClinicDoesNotExistsException()
            else:
                request.user.clinic.remove(clinic)
                request.user.save()
                return Response({}, status=status.HTTP_200_OK)
        except Clinic.DoesNotExist:
            raise ClinicDoesNotExistsException()


class PatientDoctorClinicView(ListAPIView):
    """
    View for getting patient's and doctor's common clinics.

    **Example requests**:

        GET /patient/{id}/doctor/{id}/clinic/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission,)
    serializer_class = ClinicSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(pk=self.kwargs['doctor_id'])
        doctor_clinics = doctor.clinic.all()
        patient_clinics = self.request.user.clinic.filter(is_active=True)

        common_clinics = []
        for clinic in patient_clinics:
            if clinic in doctor_clinics:
                common_clinics.append(clinic)
        return common_clinics
