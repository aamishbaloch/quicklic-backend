from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.serializers import PatientSerializer, PatientLoginSerializer

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
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    View for login a user to your system.

    **Example requests**:

        POST /api/auth/login/
    """

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(email=email, password=password)
        if user:
            if user.role == User.Role.PATIENT:
                serializer = PatientLoginSerializer(user)
            else:
                serializer = PatientLoginSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)
