from django.contrib.auth import get_user_model
from rest_framework import serializers
from libs.jwt_helper import JWTHelper

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}, 'role':{'read_only': True}}

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