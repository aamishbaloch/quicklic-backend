from django.contrib import admin
from entities.notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'type', 'patient', 'doctor', 'clinic', 'is_read')

admin.site.register(Notification, NotificationAdmin)
