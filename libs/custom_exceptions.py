from rest_framework.exceptions import APIException


class AlreadyExistsException(APIException):
    status_code = 409
    default_detail = "Object Already Exists"


class InvalidInputDataException(APIException):
    status_code = 400
    default_detail = "Invalid Input Data"


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = "Invalid Credentials"


class AppointmentDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "Appointment Does Not Exists"


class ClinicDoesNotExistsException(APIException):
    status_code = 404
    default_detail = "Clinic Does Not Exists"


class PatientExistsException(AlreadyExistsException):
    default_detail = "Patient Already Exists"
