from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView

from entities.appointment.models import AppointmentReason
from entities.clinic.models import City, Country
from entities.resources.models import Occupation, Service, Specialization
from api.v1.serializers import OccupationSerializer, ServiceSerializer, SpecializationSerializer, CitySerializer, \
    CountrySerializer, AppointmentReasonSerializer

User = get_user_model()


class CityView(ListAPIView):
    """
    View for getting all cities.

    **Example requests**:

        GET /city/
    """
    serializer_class = CitySerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return City.objects.filter(is_active=True, name__istartswith=query).order_by('id')


class CountryView(ListAPIView):
    """
    View for getting all countries.

    **Example requests**:

        GET /countries/
    """
    serializer_class = CountrySerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return Country.objects.filter(is_active=True, name__istartswith=query).order_by('id')


class OccupationView(ListAPIView):
    """
    View for getting all occupations.

    **Example requests**:

        GET /occupation/
    """
    serializer_class = OccupationSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return Occupation.objects.filter(is_active=True, name__istartswith=query).order_by('id')


class ServiceView(ListAPIView):
    """
    View for getting all services.

    **Example requests**:

        GET /service/
    """
    serializer_class = ServiceSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return Service.objects.filter(is_active=True, name__istartswith=query).order_by('id')


class SpecializationView(ListAPIView):
    """
    View for getting all specializations.

    **Example requests**:

        GET /specialization/
    """
    serializer_class = SpecializationSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return Specialization.objects.filter(is_active=True, name__istartswith=query).order_by('id')


class AppointmentReasonView(ListAPIView):
    """
    View for getting all appointment reasons.

    **Example requests**:

        GET /reason/
    """
    serializer_class = AppointmentReasonSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return AppointmentReason.objects.filter(is_active=True, name__istartswith=query).order_by('id')
