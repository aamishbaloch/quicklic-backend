from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers import PatientTokenSerializer, DoctorTokenSerializer, PatientSerializer
from entities.person.models import VerificationCode
from libs.authentication import UserAuthentication
from libs.custom_exceptions import (
    InvalidInputDataException,
    InvalidCredentialsException,
    PatientExistsException,
    InvalidVerificationCodeException,
    UserNotAllowedException,
    UserDoesNotExistsException,
    VerificationException
)
from libs.error_reports import send_manually_error_email
from libs.onesignal_sdk import OneSignalSdk
from libs.twilio_helper import TwilioHelper
from libs.permission import PatientPermission

User = get_user_model()


class RegistrationView(APIView):
    """
    View for registering a new user to your system.

    IMPORTANT: View is used to register new PATIENTS only to the app.

    **Example requests**:

        POST /auth/register/
    """

    @transaction.atomic()
    def post(self, request):
        device_id = request.data.get('device_id', None)
        device_type = request.data.get('device_type', None)

        if not User.is_exists(request.data['phone']):
            serializer = PatientTokenSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                try:
                    patient = serializer.save()
                    patient.update_device_information(device_id, device_type)

                    code = VerificationCode.generate_code_for_user(patient)
                    try:
                        TwilioHelper().message(
                            patient.phone,
                            "Welcome to Quicklic! Your Code is {}.".format(code)
                        )
                    except Exception as e:
                        send_manually_error_email("Unable to send code. Code is {}".format(code))
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    raise PatientExistsException()
            raise InvalidInputDataException(str(serializer.errors))
        raise PatientExistsException()


class LoginView(APIView):
    """
    View for login a user to your system.

    **Example requests**:

        POST /api/auth/login/
    """

    def post(self, request):
        phone = request.data.get('phone', None)
        password = request.data.get('password', None)
        device_id = request.data.get('device_id', None)
        device_type = request.data.get('device_type', None)

        user = authenticate(phone=phone, password=password)
        if user:
            user.update_device_information(device_id, device_type)
            if hasattr(user, 'doctor'):
                serializer = DoctorTokenSerializer(user.doctor, context={"request": request})
            elif hasattr(user, 'patient'):
                serializer = PatientTokenSerializer(user.patient, context={"request": request})
            else:
                raise UserNotAllowedException()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidCredentialsException()


class VerificationView(APIView):
    """
    View for verifying a user to your system.

    **Example requests**:

        POST /api/auth/verify/
    """

    authentication_classes = (UserAuthentication,)
    permission_classes = (PatientPermission,)

    def post(self, request):
        code = request.data.get('code', None)

        if request.user.verification_code:
            if request.user.verification_code.code == code:
                request.user.verified = True
                request.user.save(update_fields=['verified'])
                return Response({}, status=status.HTTP_200_OK)
        raise InvalidVerificationCodeException()


class ForgotPasswordView(APIView):
    """
    View for creating forgot code of user.

    **Example requests**:

        POST /api/auth/forgot_password/
    """
    def post(self, request):
        phone = request.data.get('phone', None)

        try:
            user = User.objects.get(phone=phone)
            if user.verified:
                code = VerificationCode.generate_code_for_user(user)
                try:
                    TwilioHelper().message(
                        user.phone,
                        "Hello from Quicklic! Your Code is {}.".format(code)
                    )
                except Exception as e:
                    send_manually_error_email("Unable to send code. Code is {}".format(code))
                return Response(None, status=status.HTTP_200_OK)
            raise VerificationException()
        except User.DoesNotExist:
            raise UserDoesNotExistsException()


class ChangePasswordVerificationView(APIView):
    """
    View for verifying a user to change the password.

    **Example requests**:

        POST /api/auth/password/verify/
    """
    def post(self, request):
        code = request.data.get('code', None)
        phone = request.data.get('phone', None)

        try:
            user = User.objects.get(phone=phone)
            if user.verified:
                if user.verification_code:
                    if user.verification_code.code == code:
                        return Response({}, status=status.HTTP_200_OK)
                    raise InvalidVerificationCodeException()
            raise VerificationException()
        except User.DoesNotExist:
            raise UserDoesNotExistsException()


class ChangePasswordView(APIView):
    """
    View for changing password with code.

    **Example requests**:

        POST /api/auth/password/change/
    """
    def post(self, request):
        code = request.data.get('code', None)
        phone = request.data.get('phone', None)
        password = request.data.get('password', None)

        try:
            user = User.objects.get(phone=phone)
            if user.verified:
                if user.verification_code:
                    if user.verification_code.code == code:
                        user.set_password(password)
                        user.save()
                        return Response({}, status=status.HTTP_200_OK)
                    raise InvalidVerificationCodeException()
            raise VerificationException()
        except User.DoesNotExist:
            raise UserDoesNotExistsException()
