from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from entities.person.models import VerificationCode

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'gender', 'is_staff', 'role', 'is_superuser', 'dob',
                  'avatar', 'verified')

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


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(OrigUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_filter = ('first_name', 'last_name','phone', 'email', 'dob', 'verified')
    list_display = (
        'id', 'first_name', 'last_name', 'verified', 'phone', 'email', 'gender', 'role', 'avatar', 'is_active',
        'is_staff', 'is_superuser', 'last_login', 'joined_on')
    ordering = ('first_name',)
    fieldsets = (
        (_('Personal Info'), {
            'fields': (
                'phone', 'verified', 'email', 'first_name', 'last_name', 'gender', 'role', 'avatar'
            )
        }),
        (_('Permissions Info'), {'fields': ('is_active', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'joined_on')}),
        ('Password Info', {'fields': ('password',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'verified', 'email', 'password1', 'password2', 'dob', 'role', 'gender', 'avatar')}
         ),
    )


admin.site.register(User, UserAdmin)


class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'user')

admin.site.register(VerificationCode, VerificationCodeAdmin)
