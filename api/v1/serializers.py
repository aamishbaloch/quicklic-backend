from django.contrib.auth import get_user_model
from rest_framework import serializers

from entities.clinic.models import City, Country, Clinic
from entities.profile_item.models import DoctorProfile, Specialization, Service, Occupation, PatientProfile
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


class PatientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.IntegerField()
    avatar = serializers.FileField(required=False, allow_null=True)
    address = serializers.CharField(max_length=500, required=False, allow_null=True)
    phone = serializers.CharField(max_length=15)
    dob = serializers.DateField()
    city = CitySerializer(source='patient_profile.city', required=False, allow_null=True)
    country = CountrySerializer(source='patient_profile.country', required=False, allow_null=True)
    occupation = OccupationSerializer(source='patient_profile.occupation', required=False, allow_null=True)
    marital_status = serializers.IntegerField(source='patient_profile.marital_status', required=False, allow_null=True)

    def create(self, validated_data):
        validated_data['role'] = User.Role.PATIENT
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        data = {'patient': user}
        PatientProfile.objects.create(**data)
        return user

    def update(self, instance, validated_data):
        validated_data['role'] = User.Role.PATIENT

        instance.first_name = validated_data['first_name'] if 'first_name' in validated_data else instance.first_name
        instance.last_name = validated_data['last_name'] if 'last_name' in validated_data else instance.last_name
        instance.gender = validated_data['gender'] if 'gender' in validated_data else instance.gender
        instance.avatar = validated_data['avatar'] if 'avatar' in validated_data else instance.avatar
        instance.address = validated_data['address'] if 'address' in validated_data else instance.address
        instance.phone = validated_data['phone'] if 'phone' in validated_data else instance.phone
        instance.dob = validated_data['dob'] if 'dob' in validated_data else instance.dob

        if 'city' in validated_data:
            city = City.objects.get(id=validated_data['city'])
            instance.patient_profile.city = city

        if 'country' in validated_data:
            country = Country.objects.get(id=validated_data['country'])
            instance.patient_profile.country = country

        if 'occupation' in validated_data:
            occupation = Occupation.objects.get(id=validated_data['occupation'])
            instance.patient_profile.occupation = occupation

        if 'marital_status' in validated_data:
            marital_status = City.objects.get(id=validated_data['marital_status'])
            instance.patient_profile.marital_status = marital_status

        instance.patient_profile.marital_status = validated_data['marital_status'] if 'marital_status' in validated_data else instance.patient_profile.marital_status
        instance.save()

        return instance


class PatientUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.IntegerField()
    avatar = serializers.FileField(required=False, allow_null=True)
    address = serializers.CharField(max_length=500, required=False, allow_null=True)
    phone = serializers.CharField(max_length=15)
    dob = serializers.DateField()
    city = serializers.IntegerField(required=False, allow_null=True)
    country = serializers.IntegerField(required=False, allow_null=True)
    occupation = serializers.IntegerField(required=False, allow_null=True)
    marital_status = serializers.IntegerField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        validated_data['role'] = User.Role.PATIENT

        instance.first_name = validated_data['first_name'] if 'first_name' in validated_data else instance.first_name
        instance.last_name = validated_data['last_name'] if 'last_name' in validated_data else instance.last_name
        instance.gender = validated_data['gender'] if 'gender' in validated_data else instance.gender
        instance.avatar = validated_data['avatar'] if 'avatar' in validated_data else instance.avatar
        instance.address = validated_data['address'] if 'address' in validated_data else instance.address
        instance.phone = validated_data['phone'] if 'phone' in validated_data else instance.phone
        instance.dob = validated_data['dob'] if 'dob' in validated_data else instance.dob

        if 'city' in validated_data and validated_data['city']:
            city = City.objects.get(id=validated_data['city'])
            instance.patient_profile.city = city

        if 'country' in validated_data and validated_data['country']:
            country = Country.objects.get(id=validated_data['country'])
            instance.patient_profile.country = country

        if 'occupation' in validated_data and validated_data['occupation']:
            occupation = Occupation.objects.get(id=validated_data['occupation'])
            instance.patient_profile.occupation = occupation

        instance.patient_profile.marital_status = validated_data['marital_status'] if 'marital_status' in validated_data else instance.patient_profile.marital_status
        instance.save()

        return instance


class PatientLoginSerializer(PatientSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        user = JWTHelper.encode_token(user)
        return user


