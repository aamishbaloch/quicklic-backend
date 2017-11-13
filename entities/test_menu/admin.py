from django.contrib import admin
from entities.test_menu.models import Test


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'clinic', 'is_common')

admin.site.register(Test, TestAdmin)
