from django.contrib import admin
from entities.appointment.models import Appointment, AppointmentReason, Visit


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'qid', 'patient', 'doctor', 'clinic', 'status']
    search_fields = ('qid',)
    list_filter = ('clinic__name', 'status')


admin.site.register(Appointment, AppointmentAdmin)


class AppointmentVisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'patient', 'doctor', 'clinic']
    search_fields = ('id', 'appointment__qid')
    list_filter = ('clinic__name',)


admin.site.register(Visit, AppointmentVisitAdmin)
