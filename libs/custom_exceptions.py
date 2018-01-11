from rest_framework.exceptions import APIException

from libs.error_reports import send_manually_error_email


class AlreadyExistsException(APIException):
    status_code = 409
    default_detail = "Already Exists"


class InvalidInputDataException(APIException):
    status_code = 400
    default_detail = "Invalid Input Data"

    def __init__(self, message=None, *args, **kwargs):
        send_manually_error_email(message)
        super(InvalidInputDataException, self).__init__(*args, **kwargs)


class InvalidVerificationCodeException(APIException):
    status_code = 400
    default_detail = "Invalid Verification Data"


class VerificationException(APIException):
    status_code = 400
    default_detail = "User Not Verified"


class DoctorUnavailableException(APIException):
    status_code = 400
    default_detail = "Doctor Not Available"


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = "Invalid Credentials"


class UserNotAllowedException(APIException):
    status_code = 401
    default_detail = "User Not Allowed"


class AppointmentDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "Appointment Does Not Exists"


class ClinicDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "Clinic Does Not Exists"


class ClinicAlreadyAddedException(AlreadyExistsException):
    default_detail = "Clinic Already Added"


class PatientExistsException(AlreadyExistsException):
    default_detail = "Patient Already Exists"


class InvalidAppointmentStatusException(APIException):
    status_code = 400
    default_detail = "Invalid Input Data"

    def __init__(self, message=None, *args, **kwargs):
        send_manually_error_email(message)
        super(InvalidAppointmentStatusException, self).__init__(*args, **kwargs)


class UserDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "User Does Not Exists"


class DoctorDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "Doctor Does Not Exists"


class PatientDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "Patient Does Not Exists"


class InvalidDateTimeException(APIException):
    status_code = 400
    default_detail = "Invalid Date Time"


class NotificationDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "Notification Does Not Exists"
