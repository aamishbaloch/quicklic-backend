from django.contrib.auth import get_user_model
from rest_framework import serializers
from entities.clinic.models import City, Country, Clinic
from entities.person.models import Doctor, Patient
from entities.resources.models import Specialization, Service, Occupation
from entities.appointment.models import Appointment, AppointmentReason
from libs.utils import get_qid_code
from libs.jwt_helper import JWTHelper

User = get_user_model()


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
    code = serializers.CharField(write_only=True)
    city = CitySerializer()
    country = CountrySerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = '__all__'

    def get_image(self, clinic):
        request = self.context.get('request')
        url = clinic.image.url
        return request.build_absolute_uri(url)


class BasicClinicSerializer(ClinicSerializer):
    class Meta:
        model = Clinic
        fields = ('id', 'name', 'image')


class DoctorSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    city = CitySerializer()
    country = CountrySerializer()
    clinic = BasicClinicSerializer(many=True)
    services = ServiceSerializer(many=True)
    specialization = SpecializationSerializer()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions')

    def get_avatar(self, doctor):
        request = self.context.get('request')
        if doctor.avatar:
            url = doctor.avatar.url
            return request.build_absolute_uri(url)


class DoctorTokenSerializer(DoctorSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, doctor):
        doctor = JWTHelper.encode_token(doctor)
        return doctor


class PatientSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    clinic = BasicClinicSerializer(many=True, required=False)
    occupation = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions')

    def get_avatar(self, doctor):
        request = self.context.get('request')
        if doctor.avatar:
            url = doctor.avatar.url
            return request.build_absolute_uri(url)

    def to_representation(self, instance):
        data = super(PatientSerializer, self).to_representation(instance)
        if instance.city:
            data['city'] = CitySerializer(instance.city).data
        if instance.city:
            data['country'] = CountrySerializer(instance.country).data
        if instance.city:
            data['occupation'] = OccupationSerializer(instance.occupation).data
        return data

    def to_internal_value(self, data):
        data = super(PatientSerializer, self).to_internal_value(data)
        if 'city' in data:
            if data['city']:
                city, created = City.objects.get_or_create(name=data['city'])
                data['city'] = city
            else:
                data['city'] = None
        if 'country' in data:
            if data['country']:
                country, created = Country.objects.get_or_create(name=data['country'])
                data['country'] = country
            else:
                data['country'] = None
        if 'occupation' in data:
            if data['occupation']:
                occupation, created = Occupation.objects.get_or_create(name=data['occupation'])
                data['occupation'] = occupation
            else:
                data['occupation'] = None
        return data

    def get_extra_kwargs(self):
        extra_kwargs = super(PatientSerializer, self).get_extra_kwargs()
        if self.instance is None:
            kwargs = extra_kwargs.get('password', {})
            kwargs['required'] = True
            extra_kwargs['password'] = kwargs
        else:
            kwargs = extra_kwargs.get('password', {})
            kwargs['required'] = False
            extra_kwargs['password'] = kwargs
            kwargs = extra_kwargs.get('phone', {})
            kwargs['read_only'] = True
            extra_kwargs['phone'] = kwargs

        return extra_kwargs

    def create(self, validated_data):
        instance = super(PatientSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class PatientTokenSerializer(PatientSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, patient):
        patient = JWTHelper.encode_token(patient)
        return patient


class AppointmentSerializer(serializers.ModelSerializer):
    qid = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False)
    reason = serializers.CharField()
    patient = PatientSerializer()
    doctor = DoctorSerializer()
    clinic = ClinicSerializer()

    class Meta:
        model = Appointment
        fields = [
            'id', 'qid', 'patient', 'doctor', 'clinic', 'start_datetime',
            'end_datetime', 'reason', 'status', 'is_active', 'created_at'
        ]

    def create(self, validated_data):
        validated_data['status'] = Appointment.Status.PENDING

        validated_data['qid'] = "{}-{}-{}".format(validated_data['patient'].id, validated_data['doctor'].id, get_qid_code())

        reason, created = AppointmentReason.objects.get_or_create(name=validated_data['reason'])
        validated_data['reason'] = reason

        appointment = Appointment.objects.create(**validated_data)

        return appointment




