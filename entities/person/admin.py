from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
from django.utils.translation import ugettext_lazy as _

from entities.person.models import VerificationCode, Doctor, Patient, DoctorSetting, Moderator, DoctorHoliday

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'gender', 'is_staff', 'is_superuser', 'dob',
                  'avatar', 'verified')
        readonly_fields = ('dob',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(OrigUserAdmin):
    add_form = UserCreationForm
    search_fields = ('phone',)
    list_filter = ('verified',)
    list_display = (
        'id', 'first_name', 'last_name', 'verified', 'phone', 'email', 'gender', 'avatar', 'is_active',
        'is_staff', 'is_superuser', 'last_login', 'joined_on', 'device_id', 'device_type')
    ordering = ('first_name',)
    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'phone', 'verified', 'email', 'first_name', 'last_name', 'gender', 'avatar', 'city', 'country',
                'clinic', 'device_id', 'device_type'
            )
        }),
        (_('Permissions Info'), {'fields': ('is_active', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'joined_on')}),
        ('Password Info', {'fields': ('password',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'verified', 'email', 'password1', 'password2',
                       'city', 'country', 'clinic', 'dob', 'gender', 'avatar', 'device_id', 'device_type')}
         ),
    )


admin.site.register(User, UserAdmin)


class Admin(UserAdmin):
    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'phone', 'first_name', 'last_name', 'verified', 'email', 'dob',
                'gender', 'avatar', 'clinic', 'city', 'country'
            )
        }),
        (_('Permissions Info'), {'fields': ('is_active', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'joined_on')}),
        ('Password Info', {'fields': ('password',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'verified', 'email', 'password1', 'password2', 'dob',
                       'gender', 'avatar', 'clinic', 'city', 'country')}
         ),
    )

admin.site.register(Moderator, Admin)


class DoctorAdmin(UserAdmin):
    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'phone', 'first_name', 'last_name', 'verified', 'email', 'dob', 'rating',
                'gender', 'avatar', 'clinic', 'city', 'country', 'services', 'specialization', 'degree',
                'device_id', 'device_type',
            )
        }),
        (_('Permissions Info'), {'fields': ('is_active', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'joined_on')}),
        ('Password Info', {'fields': ('password',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'verified', 'email', 'password1', 'password2', 'dob',
                       'gender', 'avatar', 'clinic', 'city', 'country', 'services', 'specialization', 'degree',
                       'rating')}
         ),
    )

admin.site.register(Doctor, DoctorAdmin)


class DoctorSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot_time', 'physician')
    search_fields = ('physician__phone',)

admin.site.register(DoctorSetting, DoctorSettingAdmin)


class DoctorHolidaysAdmin(admin.ModelAdmin):
    list_display = ('id', 'day')
    search_fields = ('physician__phone',)

admin.site.register(DoctorHoliday, DoctorHolidaysAdmin)


class PatientAdmin(UserAdmin):
    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'phone', 'first_name', 'last_name', 'verified', 'email', 'dob',
                'gender', 'avatar', 'clinic', 'city', 'country', 'height', 'weight', 'occupation', 'marital_status'
            )
        }),
        (_('Permissions Info'), {'fields': ('is_active', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'joined_on')}),
        ('Password Info', {'fields': ('password',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'verified', 'email', 'password1', 'password2', 'dob', 'gender',
                       'avatar', 'clinic', 'city', 'country', 'height', 'weight', 'occupation', 'marital_status')}
         ),
    )

admin.site.register(Patient, PatientAdmin)


class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'user')
    search_fields = ('user__phone',)

admin.site.register(VerificationCode, VerificationCodeAdmin)
