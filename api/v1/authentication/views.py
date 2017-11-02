from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers import PatientLoginSerializer, DoctorLoginSerializer, PatientSerializer, DoctorSerializer
from entities.person.models import VerificationCode, Doctor
from libs.authentication import UserAuthentication
from libs.custom_exceptions import InvalidInputDataException, InvalidCredentialsException, \
    PatientExistsException, InvalidVerificationCodeException
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
        serializer = PatientSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                patient = serializer.save()
                code = VerificationCode.generate_code_for_user(patient)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise PatientExistsException()
        raise InvalidInputDataException(str(serializer.errors))


class LoginView(APIView):
    """
    View for login a user to your system.

    **Example requests**:

        POST /api/auth/login/
    """

    def post(self, request):
        phone = request.data.get('phone', None)
        password = request.data.get('password', None)

        user = authenticate(phone=phone, password=password)
        if user:
            if user.doctor:
                serializer = DoctorSerializer(user.doctor, context={"request": request})
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
