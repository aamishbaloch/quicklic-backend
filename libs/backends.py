from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
    Custom user authentication backend.
    """

    def authenticate(self, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user:
                if user.check_password(password) and user.is_active:
                    return user
                return None
        except User.DoesNotExist:
            return None
