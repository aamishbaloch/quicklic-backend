from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from entities.appointment.models import Appointment, Visit
from entities.person.models import Doctor
from libs.authentication import UserAuthentication
from libs.custom_exceptions import InvalidInputDataException, InvalidAppointmentStatusException
from libs.permission import (
    DoctorPermission,
    DoctorOwnerPermission,
    AppointmentOwnerPermission,
    PatientDoctorPermission,
    PatientPermission,
    PatientBelongsDoctorPermission,
)
from libs.utils import str2bool, get_datetime_from_date_string, get_date_from_date_string, \
    get_datetime_range_from_date_string, get_interval_between_time
from api.v1.serializers import DoctorSerializer, ClinicSerializer, AppointmentSerializer, VisitSerializer

User = get_user_model()


class DoctorView(RetrieveUpdateAPIView):
    """
    View for creating and getting doctor.

    **Example requests**:

        GET /doctor/{id}
        PUT /doctor/{id}
        PATCH /doctor/{id}
    """
    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorOwnerPermission,)
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()


class DoctorListView(ListAPIView):
    """
    View for getting all doctors.

    **Example requests**:

        GET /doctor/

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
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all().order_by('id')

    def get_queryset(self):
        doctors = Doctor.objects.all().order_by('id')

        if 'clinic_id' in self.request.query_params:
            doctors = doctors.filter(clinic=self.request.query_params.get('clinic_id', None))

        if 'country_id' in self.request.query_params:
            doctors = doctors.filter(country_id=self.request.query_params.get('country_id'))

        if 'city_id' in self.request.query_params:
            doctors = doctors.filter(city_id=self.request.query_params.get('city_id'))

        if 'specialization_id' in self.request.query_params:
            doctors = doctors.filter(specialization_id=self.request.query_params.get('specialization_id'))

        if 'services_ids' in self.request.query_params:
            service_ids = [int(id) for id in self.request.query_params.get('services_ids').split(',')]
            doctors = doctors.filter(services__in=service_ids)

        if 'query' in self.request.query_params:
            doctors = doctors.filter(Q(first_name__icontains=self.request.query_params.get('query')) | Q(last_name__icontains=self.request.query_params.get('query')))

        doctors = doctors.filter(is_active=str2bool(self.request.query_params.get('active', 'true')))

        return doctors


class DoctorClinicView(ListAPIView):
    """
    View for getting doctor's clinics.

    **Example requests**:

        GET /doctor/{id}/clinic/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorOwnerPermission,)
    serializer_class = ClinicSerializer

    def get_queryset(self):
        return self.request.user.clinic.all().order_by('id')


class DoctorAppointmentView(ListAPIView):
    """
    View for getting doctor's appointments

    **Example requests**:

        GET /doctor/{id}/appointments/

    **filters**:
        - start_date
        - end_date
        - status=1
        - clinic_id=1
        - reason_id=1
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorOwnerPermission,)
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        appointments = self.request.user.doctor.appointments.all().order_by('start_datetime')

        if 'start_date' in self.request.query_params:
            start_datetime = get_datetime_from_date_string(self.request.query_params.get("start_date"))
            appointments = appointments.filter(start_datetime__gte=start_datetime)

        if 'end_date' in self.request.query_params:
            end_datetime = get_datetime_from_date_string(self.request.query_params.get("end_date"))
            appointments = appointments.filter(end_datetime__lte=end_datetime)

        if 'status' in self.request.query_params:
            statuses = [int(id) for id in self.request.query_params.get('status').split(',')]
            appointments = appointments.filter(status__in=statuses)

        if 'clinic_id' in self.request.query_params:
            appointments = appointments.filter(clinic_id=self.request.query_params.get('clinic_id'))

        if 'reason_id' in self.request.query_params:
            appointments = appointments.filter(reason_id=self.request.query_params.get('reason_id'))

        return appointments


class DoctorStatusView(APIView):
    """
    View for changing appointment status

    **Example requests**:

        POST /doctor/{id}/appointment/{appointment_id}

        **params**
        status: int
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorOwnerPermission, AppointmentOwnerPermission)

    def post(self, request, pk, appointment_id):
        status_code = request.data.get('status', None)
        if status_code:
            if status_code in [Appointment.Status.CONFIRM, Appointment.Status.DISCARD, Appointment.Status.NOSHOW]:
                appointment = Appointment.objects.get(pk=appointment_id)
                appointment.status = status_code
                appointment.save()

                return Response({}, status=status.HTTP_200_OK)
        raise InvalidAppointmentStatusException()


class DoctorAppointmentSlotView(APIView):
    """
    View for getting slots

    **Example requests**:
        GET /doctor/{id}/appointment_slots/?date=2017-06-18
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientDoctorPermission, PatientBelongsDoctorPermission)

    def get(self, request, pk):
        date = self.request.query_params.get('date', None)
        if date:
            doctor = Doctor.objects.get(pk=pk)
            start_time, end_time = doctor.setting.get_day_timings(get_date_from_date_string(date).weekday())

            intervals = get_interval_between_time(start_time, end_time, doctor.setting.slot_time, date)
            day_start, day_end = get_datetime_range_from_date_string(date)

            appointments = doctor.appointments.filter(start_datetime__gte=day_start, end_datetime__lte=day_end)
            appointments = [{
                    "start": appointment.start_datetime,
                    "end": appointment.end_datetime
                } for appointment in appointments]

            for interval in intervals:
                for appointment in appointments:
                    is_overlap = (interval['start'] <= appointment['start'] <= interval['end']) or (appointment['start'] <= interval['start'] <= appointment['end'])
                    if is_overlap:
                        interval['available'] = False

            return Response(intervals, status=status.HTTP_200_OK)

        raise InvalidInputDataException()


class DoctorVisitView(ListAPIView):
    """
    View for getting doctor visits

    **Example requests**:

        GET /doctor/{id}/visit/

        **filters**
            patient_id: Filter with patient
            clinic_id: Filter with clinic
            start_date: time filter
            end_date: time filter
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (DoctorOwnerPermission,)
    serializer_class = VisitSerializer

    def get_queryset(self):
        appointments = self.request.user.doctor.appointments.all()

        if 'clinic_id' in self.request.query_params:
            appointments = appointments.filter(clinic=self.request.query_params.get('clinic_id'))

        if 'patient_id' in self.request.query_params:
            appointments = appointments.filter(patient_id=self.request.query_params.get('patient_id'))

        if 'start_date' in self.request.query_params:
            start_datetime = get_datetime_from_date_string(self.request.query_params.get('start_date'))
            appointments = appointments.filter(start_datetime__gte=start_datetime)

        if 'end_date' in self.request.query_params:
            end_datetime = get_datetime_from_date_string(self.request.query_params.get('end_date'))
            appointments = appointments.filter(end_datetime__lte=end_datetime)

        appointment_ids = appointments.values_list('id', flat=True)

        return Visit.objects.filter(appointment_id__in=appointment_ids)


