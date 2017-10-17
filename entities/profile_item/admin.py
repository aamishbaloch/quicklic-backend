from django.contrib import admin

from entities.profile_item.models import PatientProfile, Occupation, Service, Specialization, DoctorSetting
from .models import DoctorProfile


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


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'occupation', 'country', 'city')

admin.site.register(PatientProfile, PatientProfileAdmin)


class DoctorSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'start_time', 'end_time', 'weekdays')

admin.site.register(DoctorSetting, DoctorSettingAdmin)
