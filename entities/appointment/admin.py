from django.contrib import admin
from entities.appointment.models import Appointment, AppointmentReason


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'qid', 'patient', 'doctor', 'clinic', 'status']
    search_fields = ('qid',)
    list_filter = ('clinic__name', 'status')


admin.site.register(Appointment, AppointmentAdmin)
