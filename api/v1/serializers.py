from django.contrib.auth import get_user_model
from rest_framework import serializers
from entities.clinic.models import City, Country, Clinic
from entities.person.models import Doctor, Patient
from entities.resources.models import Specialization, Service, Occupation, AppointmentReason
from entities.appointment.models import Appointment, Visit
from entities.review.models import Review
from entities.test_menu.models import Test
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


class AppointmentReasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentReason
        fields = ('id', 'name')


class ClinicSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)
    city = CitySerializer()
    country = CountrySerializer()
    rating = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Clinic
        fields = '__all__'


class BasicClinicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    rating = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Clinic
        fields = ('id', 'name', 'image', 'rating')

    def get_image(self, clinic):
        request = self.context.get('request')
        photo_url = clinic.image.url
        if photo_url:
            return request.build_absolute_uri(photo_url)


class DoctorSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    clinic = BasicClinicSerializer(many=True, required=False)
    services = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    specialization = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    verified = serializers.BooleanField(read_only=True)
    rating = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Doctor
        exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions', 'is_active')

    def to_representation(self, instance):
        data = super(DoctorSerializer, self).to_representation(instance)
        if instance.city:
            data['city'] = CitySerializer(instance.city).data
        if instance.country:
            data['country'] = CountrySerializer(instance.country).data
        if instance.specialization:
            data['specialization'] = SpecializationSerializer(instance.specialization).data
        if instance.services:
            data['services'] = ServiceSerializer(instance.services.all(), many=True).data
        return data

    def to_internal_value(self, data):
        data = super(DoctorSerializer, self).to_internal_value(data)
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
        if 'specialization' in data:
            if data['specialization']:
                specialization, created = Specialization.objects.get_or_create(name=data['specialization'])
                data['specialization'] = specialization
            else:
                data['specialization'] = None
        if 'services' in data:
            if data['services']:
                services = []
                for service in data['services'].split(","):
                    service, created = Service.objects.get_or_create(name=service)
                    services.append(service)
                data['services'] = services
            else:
                data['specialization'] = None
        return data

    def get_extra_kwargs(self):
        extra_kwargs = super(DoctorSerializer, self).get_extra_kwargs()
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

    def update(self, instance, validated_data):
        validated_data.pop('clinic')
        instance = super(DoctorSerializer, self).update(instance, validated_data)
        return instance


class BasicDoctorSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    specialization = SpecializationSerializer()
    rating = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name', 'avatar', 'phone', 'specialization', 'rating')

    def get_avatar(self, doctor):
        request = self.context.get('request')
        if doctor.avatar:
            photo_url = doctor.avatar.url
            if photo_url:
                return request.build_absolute_uri(photo_url)


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
    verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = Patient
        exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions', 'is_active')

    def to_representation(self, instance):
        data = super(PatientSerializer, self).to_representation(instance)
        if instance.city:
            data['city'] = CitySerializer(instance.city).data
        if instance.country:
            data['country'] = CountrySerializer(instance.country).data
        if instance.occupation:
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

    def update(self, instance, validated_data):
        validated_data.pop('clinic')
        instance = super(PatientSerializer, self).update(instance, validated_data)
        return instance


class BasicPatientSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'avatar', 'phone')

    def get_avatar(self, patient):
        request = self.context.get('request')
        if patient.avatar:
            photo_url = patient.avatar.url
            if photo_url:
                return request.build_absolute_uri(photo_url)


class PatientTokenSerializer(PatientSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, patient):
        patient = JWTHelper.encode_token(patient)
        return patient


class BasicVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    qid = serializers.CharField(read_only=True)
    status = serializers.IntegerField(read_only=True)
    visit = BasicVisitSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'

    def to_representation(self, instance):
        data = super(AppointmentSerializer, self).to_representation(instance)
        if instance.reason:
            data['reason'] = AppointmentReasonSerializer(instance.reason).data
        if instance.clinic:
            data['clinic'] = BasicClinicSerializer(instance.clinic, context={"request": self.context['request']}).data
        if instance.patient:
            data['patient'] = BasicPatientSerializer(instance.patient, context={"request": self.context['request']}).data
        if instance.doctor:
            data['doctor'] = BasicDoctorSerializer(instance.doctor, context={"request": self.context['request']}).data
        return data

    def create(self, validated_data):
        validated_data['status'] = Appointment.Status.PENDING

        validated_data['qid'] = "{}-{}-{}".format(validated_data['patient'].id, validated_data['doctor'].id, get_qid_code())

        reason, created = AppointmentReason.objects.get_or_create(name=validated_data['reason'])
        validated_data['reason'] = reason

        return super(AppointmentSerializer, self).create(validated_data)


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def to_representation(self, instance):
        data = super(VisitSerializer, self).to_representation(instance)

        if instance.appointment:
            data['appointment'] = AppointmentSerializer(instance.appointment).data
        if instance.clinic:
            data['clinic'] = BasicClinicSerializer(instance.clinic, context={"request": self.context['request']}).data
        if instance.patient:
            data['patient'] = BasicPatientSerializer(instance.patient, context={"request": self.context['request']}).data
        if instance.doctor:
            data['doctor'] = BasicDoctorSerializer(instance.doctor, context={"request": self.context['request']}).data
        return data


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

    def to_representation(self, instance):
        data = super(TestSerializer, self).to_representation(instance)

        if instance.clinic:
            data['clinic'] = BasicClinicSerializer(instance.clinic, context={"request": self.context['request']}).data
        return data


class ReviewSerializer(serializers.ModelSerializer):
    creator = BasicPatientSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ReviewSerializer, self).to_representation(instance)

        if instance.clinic:
            data['clinic'] = BasicClinicSerializer(instance.clinic, context={"request": self.context['request']}).data
        if instance.creator:
            data['creator'] = BasicPatientSerializer(instance.creator, context={"request": self.context['request']}).data
        if instance.doctor:
            data['doctor'] = BasicDoctorSerializer(instance.doctor, context={"request": self.context['request']}).data
        return data

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user.patient
        instance = super(ReviewSerializer, self).create(validated_data)

        if instance.type == Review.Type.DOCTOR:
            instance.doctor.calculate_rating()
        elif instance.type == Review.Type.CLINIC:
            instance.clinic.calculate_rating()

        return instance
