from django.contrib import admin
from .models import Appointment, AppointmentReason
# Register your models here.

#
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = '__all__'


admin.site.register(Appointment)


class AppointmentReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(AppointmentReason, AppointmentReasonAdmin)
