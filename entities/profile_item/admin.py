from django.contrib import admin
from .models import DoctorProfile


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'specialization', 'clinic', 'country', 'city')

admin.site.register(DoctorProfile, DoctorProfileAdmin)