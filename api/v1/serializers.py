from django.contrib.auth import get_user_model
from rest_framework import serializers
from entities.clinic.models import City, Country, Clinic
from entities.profile_item.models import DoctorProfile, Specialization, Service, Occupation, PatientProfile
from libs.jwt_helper import JWTHelper
import uuid
from entities.appointment.models import Appointment, AppointmentReason
from libs.utils import get_qid_code
from libs.utils import (
    merge_date_and_time,
    get_time_from_datetime,
    get_weekday_from_datetime
)
from entities.profile_item.models import DoctorSetting
from libs.custom_exceptions import AppointmentOverlapException


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
    city = CitySerializer()
    country = CountrySerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        fields = ('id', 'name', 'phone', 'location', 'city', 'country', 'image')

    def get_image(self, clinic):
        request = self.context.get('request')
        url = clinic.image.url
        return request.build_absolute_uri(url)


class DoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField(required=False, allow_null=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.IntegerField(required=False, allow_null=True)
    avatar = serializers.SerializerMethodField(required=False, allow_null=True)
    address = serializers.CharField(max_length=500, required=False, allow_null=True)
    phone = serializers.CharField(max_length=15)
    dob = serializers.DateField(required=False, allow_null=True)
    city = CitySerializer(source='doctor_profile.city', required=False, allow_null=True)
    country = CountrySerializer(source='doctor_profile.country', required=False, allow_null=True)
    services = ServiceSerializer(many=True, source='doctor_profile.services', required=False, allow_null=True)
    specialization = SpecializationSerializer(source='doctor_profile.specialization', required=False, allow_null=True)
    degree = serializers.CharField(source='doctor_profile.degree', required=False, allow_null=True)
    verified = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        validated_data['role'] = User.Role.DOCTOR
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        data = {'doctor': user}
        DoctorProfile.objects.create(**data)
        return user

    def get_avatar(self, doctor):
        request = self.context.get('request')
        if doctor.avatar:
            url = doctor.avatar.url
            return request.build_absolute_uri(url)


class BasicDoctorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False, allow_null=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.IntegerField(required=False, allow_null=True)
    avatar = serializers.SerializerMethodField(required=False, allow_null=True)
    address = serializers.CharField(max_length=500, required=False, allow_null=True)
    phone = serializers.CharField(max_length=15)
    services = ServiceSerializer(many=True, source='doctor_profile.services', required=False, allow_null=True)
    specialization = SpecializationSerializer(source='doctor_profile.specialization', required=False, allow_null=True)
    degree = serializers.CharField(source='doctor_profile.degree', required=False, allow_null=True)

    def get_avatar(self, doctor):
        request = self.context.get('request')
        if doctor.avatar:
            url = doctor.avatar.url
            return request.build_absolute_uri(url)


class DoctorUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField(required=False, allow_null=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    avatar = serializers.FileField(required=False, allow_null=True)
    address = serializers.CharField(max_length=500, required=False, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    services = serializers.ListField(required=False, allow_null=True)
    specialization = serializers.CharField(required=False, allow_null=True)
    degree = serializers.CharField(source='doctor_profile.degree', required=False, allow_null=True)
    verified = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        validated_data['role'] = User.Role.DOCTOR

        instance.first_name = validated_data['first_name'] if 'first_name' in validated_data else instance.first_name
        instance.last_name = validated_data['last_name'] if 'last_name' in validated_data else instance.last_name
        instance.avatar = validated_data['avatar'] if 'avatar' in validated_data else instance.avatar
        instance.address = validated_data['address'] if 'address' in validated_data else instance.address
        instance.dob = validated_data['dob'] if 'dob' in validated_data else instance.dob
        instance.save()

        if 'city' in validated_data and validated_data['city']:
            city, created = City.objects.get_or_create(name=validated_data['city'])
            instance.doctor_profile.city = city

        if 'country' in validated_data and validated_data['country']:
            country, created = Country.objects.get_or_create(name=validated_data['country'])
            instance.doctor_profile.country = country

        if 'specialization' in validated_data and validated_data['specialization']:
            specialization, created = Specialization.objects.get_or_create(name=validated_data['specialization'])
            instance.doctor_profile.specialization = specialization

        if 'services' in validated_data and validated_data['services']:
            instance.doctor_profile.services.clear()

            for service_id in validated_data['services']:
                service, created = Service.objects.get_or_create(name=service_id)
                instance.doctor_profile.services.add(service)

        instance.doctor_profile.degree = validated_data['degree'] if 'degree' in validated_data else instance.doctor_profile.degree
        instance.doctor_profile.save()

        return instance


class DoctorLoginSerializer(DoctorSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        user = JWTHelper.encode_token(user)
        return user


class PatientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField(required=False, allow_null=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.IntegerField(required=False, allow_null=True)
    avatar = serializers.SerializerMethodField(required=False, allow_null=True)
    address = serializers.CharField(max_length=500, required=False, allow_null=True)
    phone = serializers.CharField(max_length=15)
    dob = serializers.DateField(required=False, allow_null=True)
    height = serializers.FloatField(source='patient_profile.height', required=False, allow_null=True)
    weight = serializers.FloatField(source='patient_profile.weight', required=False, allow_null=True)
    city = CitySerializer(source='patient_profile.city', required=False, allow_null=True)
    country = CountrySerializer(source='patient_profile.country', required=False, allow_null=True)
    occupation = OccupationSerializer(source='patient_profile.occupation', required=False, allow_null=True)
    marital_status = serializers.IntegerField(source='patient_profile.marital_status', required=False, allow_null=True)
    verified = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        validated_data['role'] = User.Role.PATIENT
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_avatar(self, patient):
        request = self.context.get('request')
        if patient.avatar:
            url = patient.avatar.url
            return request.build_absolute_uri(url)


class BasicPatientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False, allow_null=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.IntegerField(required=False, allow_null=True)
    avatar = serializers.SerializerMethodField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=15)
    occupation = OccupationSerializer(source='patient_profile.occupation', required=False, allow_null=True)

    def get_avatar(self, patient):
        request = self.context.get('request')
        if patient.avatar:
            url = patient.avatar.url
            return request.build_absolute_uri(url)


class PatientUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    first_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False, allow_null=True)
    last_name = serializers.CharField(max_length=255)
    avatar = serializers.FileField(required=False, allow_null=True)
    address = serializers.CharField(max_length=500, required=False, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)
    height = serializers.FloatField(required=False, allow_null=True)
    weight = serializers.FloatField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    occupation = serializers.CharField(required=False, allow_null=True)
    marital_status = serializers.IntegerField(required=False, allow_null=True)
    verified = serializers.BooleanField(read_only=True)

    def update(self, instance, validated_data):
        validated_data['role'] = User.Role.PATIENT

        instance.first_name = validated_data['first_name'] if 'first_name' in validated_data else instance.first_name
        instance.last_name = validated_data['last_name'] if 'last_name' in validated_data else instance.last_name
        instance.avatar = validated_data['avatar'] if 'avatar' in validated_data else instance.avatar
        instance.address = validated_data['address'] if 'address' in validated_data else instance.address
        instance.email = validated_data['email'] if 'email' in validated_data else instance.email
        instance.dob = validated_data['dob'] if 'dob' in validated_data else instance.dob
        instance.save()

        if 'city' in validated_data and validated_data['city']:
            city, created = City.objects.get_or_create(name=validated_data['city'])
            instance.patient_profile.city = city

        if 'country' in validated_data and validated_data['country']:
            country, created = Country.objects.get_or_create(name=validated_data['country'])
            instance.patient_profile.country = country

        if 'occupation' in validated_data and validated_data['occupation']:
            occupation, created = Occupation.objects.get_or_create(name=validated_data['occupation'])
            instance.patient_profile.occupation = occupation

        instance.patient_profile.marital_status = validated_data['marital_status'] if 'marital_status' in validated_data else instance.patient_profile.marital_status
        instance.patient_profile.height = validated_data['height'] if 'height' in validated_data else instance.patient_profile.height
        instance.patient_profile.weight = validated_data['weight'] if 'weight' in validated_data else instance.patient_profile.weight
        instance.patient_profile.save()

        return instance


class PatientLoginSerializer(PatientSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        user = JWTHelper.encode_token(user)
        return user


class AppointmentSerializer(serializers.ModelSerializer):
    qid = serializers.CharField(required=False, read_only=True)
    status = serializers.CharField(required=False)
    reason = serializers.CharField()

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

        appointment_start_datetime = validated_data.pop('start_datetime')
        appointment_end_datetime = validated_data.pop('end_datetime')

        doctor = validated_data.pop('doctor')
        reason = validated_data.pop('reason')
        clinic = validated_data.pop('clinic')
        patient = validated_data.pop('patient')

        doc_setting_obj = DoctorSetting.objects.filter(doctor=doctor).first()

        if doc_setting_obj and doc_setting_obj.weekdays[get_weekday_from_datetime(appointment_start_datetime)]:
            doctor_start_time = doc_setting_obj.start_time
            doctor_end_time = doc_setting_obj.end_time

            doctor_start_datetime = merge_date_and_time(appointment_start_datetime, doctor_start_time)
            doctor_end_datetime = merge_date_and_time(appointment_start_datetime, doctor_end_time)

            appointments = Appointment.objects.filter(
                doctor=doctor,
                start_datetime__gte=doctor_start_datetime,
                end_datetime__lte=doctor_end_datetime,
                status=1
            )

            for appointment in appointments:
                start = appointment.start_datetime
                end = appointment.end_datetime
                # (StartDate1 <= EndDate2) and (StartDate2 <= EndDate1)
                time_range_overlap = max(appointment_start_datetime, start) < min(appointment_end_datetime, end)
                if time_range_overlap:
                    raise AppointmentOverlapException

            return Appointment.objects.create(
                patient=patient,
                reason=reason,
                clinic=clinic,
                doctor=doctor,
                is_active=True,
                start_datetime=appointment_start_datetime,
                end_datetime=appointment_end_datetime,
                **validated_data
            )

        return Appointment()

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance

