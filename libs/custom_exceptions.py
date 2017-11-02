from rest_framework.exceptions import APIException

from libs.error_reports import send_manually_error_email


class AlreadyExistsException(APIException):
    status_code = 409
    default_detail = "Object Already Exists"


class InvalidInputDataException(APIException):
    status_code = 400
    default_detail = "Invalid Input Data"

    def __init__(self, message=None, *args, **kwargs):
        send_manually_error_email(message)
        super(InvalidInputDataException, self).__init__(*args, **kwargs)


class InvalidVerificationCodeException(APIException):
    status_code = 400
    default_detail = "Invalid Verification Data"


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = "Invalid Credentials"


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


class AppointmentOverlapException(APIException):
    status_code = 404
    default_detail = "This time is already appointed. Please select other timings."

