from rest_framework import serializers
import uuid
from entities.appointment.models import Appointment
from entities.profile_item.models import DoctorSetting


class AppointmentSerializer(serializers.ModelSerializer):
    qid = serializers.UUIDField(default=uuid.uuid4())
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = Appointment
        fields = [
            'id', 'qid', 'patient', 'doctor', 'clinic', 'start_datetime',
            'end_datetime', 'duration', 'reason', 'status', 'is_active', 'created_at'
        ]

    def create(self, validated_data):

        appointment_start_datetime = validated_data['start_datetime']
        appointment_end_datetime = validated_data['end_datetime']
        doctor = validated_data.pop('doctor')
        reason = validated_data.pop('reason')
        clinic = validated_data.pop('clinic')

        doc_setting = DoctorSetting.objects.filter(doctor__doctor_id=doctor).first()
        doctor_start_datetime = doc_setting.start_datetime
        doctor_end_datetime = doc_setting.end_datetime

        appointments = Appointment.objects.filter(
            doctor=doctor,
            start_datetime__gte=doctor_start_datetime,
            end_datetime__lte=doctor_end_datetime,
            status='CONF'
        )

        if appointment_start_datetime >= doctor_start_datetime and appointment_end_datetime <= doctor_end_datetime:
            for obj in appointments:
                start = obj.start_datetime
                end = obj.end_datetime
                # (StartDate1 <= EndDate2) and (StartDate2 <= EndDate1)
                datetime_range_overlap = max(appointment_start_datetime, start) < min(appointment_end_datetime, end)
                if datetime_range_overlap:
                    return "Error: Overlap timing."

            return Appointment.objects.create(
                reason=reason,
                clinic=clinic,
                doctor=doctor,
                status='PEND',
                is_active=True,
                **validated_data
            )
        return Appointment()


