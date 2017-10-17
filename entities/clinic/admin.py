from django.contrib import admin
from .models import Clinic, Country, City


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')

admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')

admin.site.register(City, CityAdmin)


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'phone', 'city', 'country', 'is_active', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)

admin.site.register(Clinic, ClinicAdmin)