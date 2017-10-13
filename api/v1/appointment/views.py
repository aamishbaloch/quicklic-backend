from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.authentication import UserAuthentication
from libs.utils import str2bool
from api.v1.serializers import DoctorSerializer, DoctorUpdateSerializer

from rest_framework.generics import CreateAPIView
from entities.profile_item.models import PatientProfile
from .exceptions import PatientNotFoundException

User = get_user_model()


class AppointmentCreateView(CreateAPIView):

    def get_object(self):
        try:
            return PatientProfile.objects.get(user=self.request.user)
        except PatientProfile.DoesNotExist:
            raise PatientNotFoundException

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)