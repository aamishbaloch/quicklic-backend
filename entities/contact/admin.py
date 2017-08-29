from django.contrib import admin
from entities.contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'contacted', 'subject','created_at')

admin.site.register(Contact, ContactAdmin)