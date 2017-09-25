from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class DoctorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(source='user.avatar.url')

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'gender', 'avatar_url', 'address', 'phone',
                  'dob')
