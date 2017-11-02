from django.contrib import admin

from .models import Occupation, Service, Specialization, AppointmentReason


class OccupationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(Occupation, OccupationAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(Service, ServiceAdmin)


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(Specialization, SpecializationAdmin)


class AppointmentReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(AppointmentReason, AppointmentReasonAdmin)

