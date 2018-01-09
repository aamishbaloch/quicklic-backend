from django import forms

from entities.person.models import User


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
