from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from entities.clinic.models import City, Country
from entities.profile_item.models import Occupation, Service, Specialization
from libs.utils import str2bool
from api.v1.serializers import OccupationSerializer, ServiceSerializer, SpecializationSerializer, CitySerializer, \
    CountrySerializer

User = get_user_model()


class CityView(APIView):
    """
    View for getting all cities.

    **Example requests**:

        GET /city/
    """

    def get(self, request):
        cities = City.objects.filter(is_active=True)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountryView(APIView):
    """
    View for getting all countries.

    **Example requests**:

        GET /countries/
    """

    def get(self, request):
        countries = Country.objects.filter(is_active=True)
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OccupationView(APIView):
    """
    View for getting all occupations.

    **Example requests**:

        GET /occupation/
    """

    def get(self, request):
        occupations = Occupation.objects.filter(is_active=True)
        serializer = OccupationSerializer(occupations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceView(APIView):
    """
    View for getting all services.

    **Example requests**:

        GET /service/
    """

    def get(self, request):
        services = Service.objects.filter(is_active=True)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecializationView(APIView):
    """
    View for getting all specializations.

    **Example requests**:

        GET /specialization/
    """

    def get(self, request):
        specializations = Specialization.objects.filter(is_active=True)
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
