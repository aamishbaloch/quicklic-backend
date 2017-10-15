from django.contrib import admin

from entities.profile_item.models import PatientProfile, Occupation, Service, Specialization
from .models import DoctorProfile, DoctorSetting


class OccupationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(Occupation, OccupationAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(Service, ServiceAdmin)


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(Specialization, SpecializationAdmin)


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'specialization', 'country', 'city', 'degree')

admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(DoctorSetting)

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'occupation', 'country', 'city')

admin.site.register(PatientProfile, PatientProfileAdmin)