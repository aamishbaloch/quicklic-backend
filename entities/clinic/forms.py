from django import forms
from .models import Clinic


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = [
            'code', 'name', 'phone', 'email', 'website', 'location', 'city', 'country',
            'is_lab', 'is_active', 'rating', 'image'
        ]
