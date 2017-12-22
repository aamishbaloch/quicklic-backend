from django.contrib import admin
from entities.notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'heading', 'user', 'user_type', 'is_read', 'patient', 'doctor', 'clinic')

admin.site.register(Notification, NotificationAdmin)
