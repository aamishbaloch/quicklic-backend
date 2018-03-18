from django.db.models import Q
from datetime import datetime, timedelta
from entities.appointment.models import Appointment
from entities.clinic.models import Clinic
from entities.notification.models import Notification
from entities.person.models import Patient, Doctor


def _get_appointments_of_doctor_for_last_n_days(doctor, n=7):
    return Appointment.objects.filter(
        start_datetime__gte=datetime.now()-timedelta(days=n),
        end_datetime__lt=datetime.now(),
        doctor_id=doctor.id
    )


def _get_appointments_of_admin_for_last_n_days(admin, n=7):
    clinics = admin.clinic.all()
    clinic_ids = clinics.values_list('id', flat=True).distinct()
    return Appointment.objects.filter(
        start_datetime__gte=datetime.now()-timedelta(days=n),
        end_datetime__lt=datetime.now(),
        clinic_id__in=clinic_ids
    )


def get_doctor_appointment_stats(doctor):
    """
    :param doctor:
    :return:
    dict = { Stats Dict }
    """
    appointments = _get_appointments_of_doctor_for_last_n_days(doctor)
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
    appointments = _get_appointments_of_admin_for_last_n_days(admin)
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


def get_key_factors_for_doctor(doctor):
    appointments = _get_appointments_of_doctor_for_last_n_days(doctor, 14)
    appointment_count = appointments.count()
    completed_appointments = appointments.filter(status=Appointment.Status.DONE).count()

    data = {
        "patient_seen": appointments.filter(status=Appointment.Status.DONE).count(),
        "clinic_count": doctor.clinic.count(),
        "rating": doctor.rating,
        "dcr": (completed_appointments*100)/appointment_count if appointment_count > 0 else 0,
        "top_clinic_name": get_top_clinic_name_for_doctor(doctor, appointments),
    }
    return data


def get_doctor_future_holidays(doctor):
    return doctor.holidays.filter(day__gte=datetime.now().date(), day__lte=(datetime.now()+timedelta(days=14)).date()).order_by('day')


def get_top_clinic_name_for_doctor(doctor, appointments):
    top_clinic_name = "Not Found"
    clinic_appointments = 0
    for clinic in doctor.clinic.all():
        if appointments.filter(clinic_id=clinic.id).count() > clinic_appointments:
            top_clinic_name = clinic.name
    return top_clinic_name


def get_patients_for_doctor(doctor):
    clinic_ids = doctor.clinic.all().values_list("id", flat=True)
    patients = Patient.objects.filter(clinic__id__in=clinic_ids, is_active=True).distinct().order_by('first_name')
    return patients


def get_patients_for_admin(admin):
    clinic_ids = admin.clinic.all().values_list("id", flat=True)
    patients = Patient.objects.filter(clinic__id__in=clinic_ids, is_active=True).distinct().order_by('first_name')
    return patients


def get_doctors_for_admin(admin):
    clinic_ids = admin.clinic.all().values_list("id", flat=True)
    doctors = Doctor.objects.filter(clinic__id__in=clinic_ids, is_active=True).distinct().order_by('first_name')
    return doctors


def send_announcement_to_all_patients(person, message):
    """
    person can be doctor or admin
    """
    clinic_ids = person.clinic.all().values_list("id", flat=True)
    patients = Patient.objects.filter(clinic__id__in=clinic_ids, is_active=True).distinct()
    Notification.create_batch_announcement(patients, message)


def send_announcement_to_all_doctors(admin, message):
    clinic_ids = admin.clinic.all().values_list("id", flat=True)
    doctors = Doctor.objects.filter(clinic__id__in=clinic_ids, is_active=True).distinct()
    Notification.create_batch_announcement(doctors, message)
