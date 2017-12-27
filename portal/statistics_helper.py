from django.db.models import Q
from datetime import datetime, timedelta
from entities.appointment.models import Appointment
from entities.clinic.models import Clinic


def get_doctor_appointment_stats(doctor):
    """
    :param doctor_id:
    :return:
    dict = { Stats Dict }
    """
    appointments = Appointment.objects.filter(created_at__gte=datetime.now()-timedelta(days=7), doctor_id=doctor.id)
    total_count = appointments.count()

    appointment_done_count = appointments.filter(status=Appointment.Status.DONE).count()
    appointment_noshow_count = appointments.filter(status=Appointment.Status.NOSHOW).count()
    appointment_cancel_count = appointments.filter(status=Appointment.Status.CANCEL).count()
    appointment_discard_count = appointments.filter(status=Appointment.Status.DISCARD).count()
    appointment_other_count = appointments.filter(Q(status=Appointment.Status.PENDING) | Q(status=Appointment.Status.CONFIRM)).count()

    clinics = appointments.values_list('clinic_id', flat=True).distinct()
    clinic_count = clinics.count()

    appointment_clinics = []
    appointment_clinic_colors = []
    for clinic in clinics:
        clinic = Clinic.objects.get(pk=clinic)
        appointment_clinics.append({
            "id": clinic.id,
            "name": clinic.name,
            "percentage": appointments.filter(clinic_id=clinic.id).count()*100/total_count,
            "color": clinic.color,
        })
        appointment_clinic_colors.append(clinic.color)

    stats = {
        "doctor_id": doctor.id,
        "doctor_name": doctor.get_full_name(),
        "appointment_count": total_count,
        "appointment_done_count": appointment_done_count,
        "appointment_done_percentage": (appointment_done_count*100)/total_count if total_count > 0 else 0,
        "appointment_noshow_count": appointment_noshow_count,
        "appointment_noshow_percentage": (appointment_noshow_count*100)/total_count if total_count > 0 else 0,
        "appointment_cancel_count": appointment_cancel_count,
        "appointment_cancel_percentage": (appointment_cancel_count*100)/total_count if total_count > 0 else 0,
        "appointment_discard_count": appointment_discard_count,
        "appointment_discard_percentage": (appointment_discard_count*100)/total_count if total_count > 0 else 0,
        "appointment_other_count": appointment_other_count,
        "appointment_other_percentage": (appointment_other_count*100)/total_count if total_count > 0 else 0,
        "clinic_count": clinic_count,
        "clinics_appointment_count": appointment_clinics,
        "appointment_clinic_colors": appointment_clinic_colors,
    }
    return stats


def get_admin_clinic_stats(admin):
    """
    :param admin:
    :return:
    dict = { Stats Dict }
    """
    clinics = admin.clinic.all()
    clinic_ids = clinics.values_list('id', flat=True).distinct()
    appointments = Appointment.objects.filter(created_at__gte=datetime.now()-timedelta(days=7), clinic_id__in=clinic_ids)

    total_clinics_appointments = appointments.count()
    total_clinics_done_appointments = appointments.filter(status=Appointment.Status.DONE).count()
    total_clinics_noshow_appointments = appointments.filter(status=Appointment.Status.NOSHOW).count()

    clinics_data = []
    clinics_colors_data = []
    for clinic in clinics:
        clinic_appointments = appointments.filter(clinic_id=clinic.id).count()
        clinic_done_appointments = appointments.filter(clinic_id=clinic.id, status=Appointment.Status.DONE).count()
        clinic_noshow_appointments = appointments.filter(clinic_id=clinic.id, status=Appointment.Status.NOSHOW).count()

        clinics_data.append({
            "clinic_name": clinic.name,
            "clinic_id": clinic.id,
            "clinic_color": clinic.color,
            "clinic_appointment_percentage": (clinic_appointments*100)/total_clinics_appointments if total_clinics_appointments > 0 else 0,
            "clinic_appointment_done_percentage": (clinic_done_appointments*100)/total_clinics_done_appointments if total_clinics_done_appointments > 0 else 0,
            "clinic_appointment_noshow_percentage": (clinic_noshow_appointments*100)/total_clinics_noshow_appointments if total_clinics_noshow_appointments > 0 else 0,
        })
        clinics_colors_data.append(clinic.color)

    stats = {
        "admin_id": admin.id,
        "admin_name": admin.get_full_name(),
        "clinic_count": clinics.count(),
        "clinics_data": clinics_data,
        "clinics_colors_data": clinics_colors_data,
    }
    return stats

