from rest_framework.exceptions import APIException


class PatientNotFoundException(APIException):
    status_code = 404
    default_detail = 'Please login as Patient.'
