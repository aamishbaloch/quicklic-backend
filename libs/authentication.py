from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from libs.jwt_helper import JWTHelper

User = get_user_model()


class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
            if not token:
                raise exceptions.AuthenticationFailed('No token provided')
            is_valid, message = JWTHelper.is_token_valid(token)
            if is_valid:
                phone = JWTHelper.decode_token(token)
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    raise exceptions.AuthenticationFailed('No such user')
                return user, None
            raise exceptions.AuthenticationFailed(message)
        raise exceptions.AuthenticationFailed('No token provided')