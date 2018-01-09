from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.base import View
from rest_framework.views import APIView

from portal import constants
from portal.forms import LoginForm, ProfileForm
from portal.statistics_helper import get_doctor_appointment_stats, get_admin_appointment_stats

User = get_user_model()


class LoginView(TemplateView):
    template_name = "portal/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                phone=form.cleaned_data["phone"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                if hasattr(user, 'moderator') or hasattr(user, 'doctor'):
                    if user.is_active:
                        login(request, user)
                    else:
                        messages.error(request, constants.UserIsNotActive)
                        return HttpResponseRedirect(reverse('portal:login'))
                else:
                    messages.error(request, constants.UserNotAllowed)
                    return HttpResponseRedirect(reverse('portal:login'))
            else:
                messages.error(request, constants.UserIsNotAuthenticated)
                return HttpResponseRedirect(reverse('portal:login'))
        else:
            messages.error(request, constants.OPERATION_UNSUCCESSFUL)
            return HttpResponseRedirect(reverse('portal:login'))
        return HttpResponseRedirect(reverse('portal:home'))


class LogoutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('portal:login'))


class PortalHomeView(TemplateView):
    template_name = "portal/home.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('portal:login'))

        return super(PortalHomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PortalHomeView, self).get_context_data(**kwargs)
        if self.request.user.is_doctor():
            context['stats'] = get_doctor_appointment_stats(self.request.user.doctor)
        elif self.request.user.is_admin():
            context['stats'] = get_admin_appointment_stats(self.request.user.moderator)
        return context


class ProfileView(TemplateView):
    template_name = "portal/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('portal:login'))

        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        if self.request.user.is_doctor():
            context['type'] = User.Role.DOCTOR
            context['user'] = self.request.user.doctor
            context['doctor_timings'] = self.request.user.doctor.setting.get_timings_with_switch()
        elif self.request.user.is_admin():
            context['type'] = User.Role.ADMIN
            context['user'] = self.request.user.moderator
        return context

    def post(self, request):
        form = ProfileForm(request.POST, instance=self.request.user)
        if form.is_valid():
            user = form.save()
        else:
            messages.error(request, constants.OPERATION_UNSUCCESSFUL)
        return HttpResponseRedirect(reverse('portal:profile'))


class DoctorSettingView(APIView):
    def post(self, request):
        data = request.POST
        setting = self.request.user.doctor.setting

        if "monday_check" in data:
            setting.monday_start = data['monday_start']
            setting.monday_end = data['monday_end']
        else:
            setting.monday_start = "00:00"
            setting.monday_end = "00:00"

        if "tuesday_check" in data:
            setting.tuesday_start = data['tuesday_start']
            setting.tuesday_end = data['tuesday_end']
        else:
            setting.tuesday_start = "00:00"
            setting.tuesday_end = "00:00"

        if "wednesday_check" in data:
            setting.wednesday_start = data['wednesday_start']
            setting.wednesday_end = data['wednesday_end']
        else:
            setting.wednesday_start = "00:00"
            setting.wednesday_end = "00:00"

        if "thursday_check" in data:
            setting.thursday_start = data['thursday_start']
            setting.thursday_end = data['thursday_end']
        else:
            setting.thursday_start = "00:00"
            setting.thursday_end = "00:00"

        if "friday_check" in data:
            setting.friday_start = data['friday_start']
            setting.friday_end = data['friday_end']
        else:
            setting.friday_start = "00:00"
            setting.friday_end = "00:00"

        if "saturday_check" in data:
            setting.saturday_start = data['saturday_start']
            setting.saturday_end = data['saturday_end']
        else:
            setting.saturday_start = "00:00"
            setting.saturday_end = "00:00"

        if "sunday_check" in data:
            setting.sunday_start = data['sunday_start']
            setting.sunday_end = data['sunday_end']
        else:
            setting.sunday_start = "00:00"
            setting.sunday_end = "00:00"

        setting.save()
        return HttpResponseRedirect(reverse('portal:profile'))
