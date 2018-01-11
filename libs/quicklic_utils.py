from entities.appointment.models import Appointment
from entities.notification.models import Notification
from libs.utils import get_start_datetime_from_date_string, get_end_datetime_from_date_string


def cancel_appointments_of_day_and_send_notify(date_to_cancel, doctor_id):
    date_start = get_start_datetime_from_date_string(str(date_to_cancel))
    date_end = get_end_datetime_from_date_string(str(date_to_cancel))

    appointments = Appointment.objects.filter(start_datetime__gte=date_start, end_datetime__lte=date_end, doctor_id=doctor_id)
    appointments.update(status=Appointment.Status.DISCARD)

    Notification.create_batch_notification_for_discard(appointments=appointments)
