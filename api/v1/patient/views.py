from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView

from entities.appointment.models import Appointment, Visit
from entities.clinic.models import Clinic
from entities.notification.models import Notification
from entities.person.models import Patient, Doctor
from libs.authentication import UserAuthentication
from libs.custom_exceptions import ClinicDoesNotExistsException, ClinicAlreadyAddedException
from libs.permission import PatientOwnerPermission, AppointmentOwnerPermission
from libs.utils import str2bool, get_datetime_from_date_string, get_start_datetime_from_date_string, \
    get_end_datetime_from_date_string
from api.v1.serializers import (
    PatientSerializer,
    ClinicSerializer,
    AppointmentSerializer,
    DoctorSerializer,
    VisitSerializer,
    ReviewSerializer)


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
    queryset = Patient.objects.all().order_by('id')

    def get_queryset(self):
        patients = Patient.objects.all().order_by('id')

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


class PatientAppointmentView(ListAPIView):
    """
    View for getting patient's appointments

    **Example requests**:

        GET /patient/{id}/appointment/

    **filters**:
        - start_date
        - end_date
        - status=1
        - clinic_id=1
        - reason_id=1
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission,)
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        appointments = self.request.user.patient.appointments.all().order_by('start_datetime')

        if 'start_date' in self.request.query_params:
            start_datetime = get_start_datetime_from_date_string(self.request.query_params.get("start_date"))
            appointments = appointments.filter(start_datetime__gte=start_datetime)

        if 'end_date' in self.request.query_params:
            end_datetime = get_end_datetime_from_date_string(self.request.query_params.get("end_date"))
            appointments = appointments.filter(end_datetime__lt=end_datetime)

        if 'status' in self.request.query_params:
            statuses = [int(id) for id in self.request.query_params.get('status').split(',')]
            appointments = appointments.filter(status__in=statuses)

        if 'clinic_id' in self.request.query_params:
            appointments = appointments.filter(clinic_id=self.request.query_params.get('clinic_id'))

        if 'reason_id' in self.request.query_params:
            appointments = appointments.filter(reason_id=self.request.query_params.get('reason_id'))

        return appointments


class PatientAppointmentCancelView(APIView):
    """
    View for canceling appointment

    **Example requests**:

        GET /patient/{id}/appointment/{appointment_id}/cancel/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission, AppointmentOwnerPermission)

    def get(self, request, pk, appointment_id):
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment.status = Appointment.Status.CANCEL
        appointment.save()

        Notification.create_notification(
            user=appointment.doctor,
            user_type=Notification.UserType.DOCTOR,
            heading=Notification.Message.APPOINTMENT_CANCELED["heading"],
            content=Notification.Message.APPOINTMENT_CANCELED["contents"].format(
                        patient=appointment.patient.get_full_name()),
            type=Notification.Type.APPOINTMENT,
            appointment_id=appointment.id,
            patient=appointment.patient,
            doctor=appointment.doctor,
            clinic=appointment.clinic
        )

        return Response({}, status=status.HTTP_200_OK)


class PatientDoctorsView(ListAPIView):
    """
    View for getting doctors related to patient

    **Example requests**:

        GET /patient/{id}/doctor
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission,)
    serializer_class = DoctorSerializer

    def get_queryset(self):
        patient_clinics = self.request.user.clinic.filter(is_active=True).values_list('id', flat=True)
        return Doctor.objects.filter(clinic__id__in=patient_clinics).distinct().order_by('rating')


class PatientVisitView(ListAPIView):
    """
    View for getting patient visits

    **Example requests**:

        GET /patient/{id}/visit/

        **filters**
            doctor_id: Filter with doctor
            clinic_id: Filter with clinic
            start_date: time filter
            end_date: time filter
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission,)
    serializer_class = VisitSerializer

    def get_queryset(self):
        appointments = self.request.user.patient.appointments.all().order_by('-start_datetime')

        if 'clinic_id' in self.request.query_params:
            appointments = appointments.filter(clinic=self.request.query_params.get('clinic_id'))

        if 'doctor_id' in self.request.query_params:
            appointments = appointments.filter(doctor_id=self.request.query_params.get('doctor_id'))

        if 'start_date' in self.request.query_params:
            start_datetime = get_start_datetime_from_date_string(self.request.query_params.get('start_date'))
            appointments = appointments.filter(start_datetime__gte=start_datetime)

        if 'end_date' in self.request.query_params:
            end_datetime = get_end_datetime_from_date_string(self.request.query_params.get('end_date'))
            appointments = appointments.filter(end_datetime__lte=end_datetime)

        appointment_ids = appointments.values_list('id', flat=True)

        return Visit.objects.filter(appointment_id__in=appointment_ids)


class PatientReviewView(ListAPIView):
    """
    View for getting patient reviews

    **Example requests**:

        GET /patient/{id}/review/

        **filters**
            doctor_id: Filter with doctor
            clinic_id: Filter with clinic
            start_date: time filter
            end_date: time filter
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientOwnerPermission,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        reviews = self.request.user.patient.reviews.all().order_by('created_at')

        if 'clinic_id' in self.request.query_params:
            reviews = reviews.filter(clinic=self.request.query_params.get('clinic_id'))

        if 'doctor_id' in self.request.query_params:
            reviews = reviews.filter(doctor_id=self.request.query_params.get('doctor_id'))

        if 'start_date' in self.request.query_params:
            start_datetime = get_start_datetime_from_date_string(self.request.query_params.get('start_date'))
            reviews = reviews.filter(created_at__gte=start_datetime)

        if 'end_date' in self.request.query_params:
            end_datetime = get_end_datetime_from_date_string(self.request.query_params.get('end_date'))
            reviews = reviews.filter(created_at__lte=end_datetime)

        return reviews
