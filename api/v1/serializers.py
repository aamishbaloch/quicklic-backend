from django.contrib.auth import get_user_model
from rest_framework import serializers

from entities.clinic.models import City, Country, Clinic
from entities.profile_item.models import DoctorProfile, Specialization, Service, Occupation, PatientProfile
from libs.jwt_helper import JWTHelper

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'role', 'gender', 'phone', 'dob')
        extra_kwargs = {'password': {'write_only': True}, 'role': {'read_only': True}}

    def create(self, validated_data):
        validated_data['role'] = User.Role.PATIENT
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(UserSerializer):
    token = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('token',)

    def get_token(self, user):
        user = JWTHelper.encode_token(user)
        return user


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'name')


class SpecializationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialization
        fields = ('id', 'name')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('id', 'name')


class OccupationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occupation
        fields = ('id', 'name')


class ClinicSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    country = CountrySerializer()

    class Meta:
        model = Clinic
        fields = ('id', 'name', 'phone', 'location', 'city', 'country', 'image')


class DoctorProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    country = CountrySerializer()
    specialization = SpecializationSerializer()
    services = ServiceSerializer(many=True)

    class Meta:
        model = DoctorProfile
        fields = ('country', 'city', 'services', 'specialization', 'degree')


class DoctorSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'gender', 'avatar', 'address', 'phone',
                  'dob', 'doctor_profile')


class PatientProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    country = CountrySerializer()
    occupation = OccupationSerializer()

    class Meta:
        model = PatientProfile
        fields = ('country', 'city', 'occupation', 'marital_status')


class PatientSerializer(serializers.ModelSerializer):
    patient_profile = PatientProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'gender', 'avatar', 'address', 'phone',
                  'dob', 'patient_profile')


