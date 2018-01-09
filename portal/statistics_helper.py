from django.db.models import Q
from datetime import datetime, timedelta
from entities.appointment.models import Appointment
from entities.clinic.models import Clinic


def get_doctor_appointment_stats(doctor):
    """
    :param doctor:
    :return:
    dict = { Stats Dict }
    """
    appointments = Appointment.objects.filter(created_at__gte=datetime.now()-timedelta(days=7), doctor_id=doctor.id)
    total_count = appointments.count()

    appointment_done_count = appointments.filter(status=Appointment.Status.DONE).count()
    appointment_noshow_count = appointments.filter(status=Appointment.Status.NOSHOW).count()
    appointment_cancel_count = appointments.filter(status=Appointment.Status.CANCEL).count()
    appointment_discard_count = appointments.filter(status=Appointment.Status.DISCARD).count()
    appointment_pending_count = appointments.filter(status=Appointment.Status.PENDING).count()
    appointment_confirm_count = appointments.filter(status=Appointment.Status.CONFIRM).count()

    stats = {
        "user_id": doctor.id,
        "user_name": doctor.get_full_name(),
        "appointment_count": total_count,
        "appointment_done_count": appointment_done_count,
        "appointment_done_percentage": (appointment_done_count*100)/total_count if total_count > 0 else 0,
        "appointment_noshow_count": appointment_noshow_count,
        "appointment_noshow_percentage": (appointment_noshow_count*100)/total_count if total_count > 0 else 0,
        "appointment_cancel_count": appointment_cancel_count,
        "appointment_cancel_percentage": (appointment_cancel_count*100)/total_count if total_count > 0 else 0,
        "appointment_discard_count": appointment_discard_count,
        "appointment_discard_percentage": (appointment_discard_count*100)/total_count if total_count > 0 else 0,
        "appointment_pending_count": appointment_pending_count,
        "appointment_pending_percentage": (appointment_pending_count*100)/total_count if total_count > 0 else 0,
        "appointment_confirm_count": appointment_confirm_count,
        "appointment_confirm_percentage": (appointment_confirm_count*100)/total_count if total_count > 0 else 0,
    }
    return stats


def get_admin_appointment_stats(admin):
    """
    :param admin:
    :return:
    dict = { Stats Dict }
    """
    clinics = admin.clinic.all()
    clinic_ids = clinics.values_list('id', flat=True).distinct()
    appointments = Appointment.objects.filter(created_at__gte=datetime.now()-timedelta(days=7), clinic_id__in=clinic_ids)
    total_count = appointments.count()

    appointment_done_count = appointments.filter(status=Appointment.Status.DONE).count()
    appointment_noshow_count = appointments.filter(status=Appointment.Status.NOSHOW).count()
    appointment_cancel_count = appointments.filter(status=Appointment.Status.CANCEL).count()
    appointment_discard_count = appointments.filter(status=Appointment.Status.DISCARD).count()
    appointment_pending_count = appointments.filter(status=Appointment.Status.PENDING).count()
    appointment_confirm_count = appointments.filter(status=Appointment.Status.CONFIRM).count()

    stats = {
        "user_id": admin.id,
        "user_name": admin.get_full_name(),
        "appointment_count": total_count,
        "appointment_done_count": appointment_done_count,
        "appointment_done_percentage": (appointment_done_count*100)/total_count if total_count > 0 else 0,
        "appointment_noshow_count": appointment_noshow_count,
        "appointment_noshow_percentage": (appointment_noshow_count*100)/total_count if total_count > 0 else 0,
        "appointment_cancel_count": appointment_cancel_count,
        "appointment_cancel_percentage": (appointment_cancel_count*100)/total_count if total_count > 0 else 0,
        "appointment_discard_count": appointment_discard_count,
        "appointment_discard_percentage": (appointment_discard_count*100)/total_count if total_count > 0 else 0,
        "appointment_pending_count": appointment_pending_count,
        "appointment_pending_percentage": (appointment_pending_count*100)/total_count if total_count > 0 else 0,
        "appointment_confirm_count": appointment_confirm_count,
        "appointment_confirm_percentage": (appointment_confirm_count*100)/total_count if total_count > 0 else 0,
    }
    return stats


def get_doctor_ccr_stats(doctor):
    """
    ccr = Clinic Conversion Rate
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
    appointment_pending_count = appointments.filter(status=Appointment.Status.PENDING).count()
    appointment_confirm_count = appointments.filter(status=Appointment.Status.CONFIRM).count()

    clinics = appointments.values_list('clinic_id', flat=True).distinct()
    clinic_count = clinics.count()

    appointment_clinics = []
    for clinic in clinics:
        clinic = Clinic.objects.get(pk=clinic)
        appointment_clinics.append({
            "id": clinic.id,
            "name": clinic.name,
            "percentage": appointments.filter(clinic_id=clinic.id).count()*100/total_count if total_count > 0 else 0,
            "color": clinic.color,
        })

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
        "appointment_pending_count": appointment_discard_count,
        "appointment_pending_percentage": (appointment_discard_count*100)/total_count if total_count > 0 else 0,
        "appointment_confirm_count": appointment_discard_count,
        "appointment_confirm_percentage": (appointment_discard_count*100)/total_count if total_count > 0 else 0,
        "clinic_count": clinic_count,
        "clinics_appointment_count": appointment_clinics,
    }
    return stats
