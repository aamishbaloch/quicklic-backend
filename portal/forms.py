from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


