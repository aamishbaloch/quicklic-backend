from django.contrib import admin
from entities.appointment.models import Appointment, AppointmentReason


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'qid', 'patient', 'doctor']


admin.site.register(Appointment, AppointmentAdmin)


class AppointmentReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(AppointmentReason, AppointmentReasonAdmin)
