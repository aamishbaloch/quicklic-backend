from django import forms

from entities.person.models import User, DoctorHoliday


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class DoctorHolidayForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorHolidayForm, self).__init__(*args, **kwargs)
        self.fields['notes'].required = False
        self.fields['day'].input_formats = ['%d-%m-%Y']

    class Meta:
        model = DoctorHoliday
        fields = ['physician', 'day', 'notes']

