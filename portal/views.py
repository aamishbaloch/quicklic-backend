from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
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

    @transaction.atomic()
    def post(self, request):
        data = request.POST
        setting = self.request.user.doctor.setting

        previous_timings = setting.get_timings_with_switch()

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

        if previous_timings['monday']['start'] != setting.monday_start or previous_timings['monday']['end'] != setting.monday_end:
            self.request.user.doctor.cancel_appointment_due_to_time_changed(0)
        elif previous_timings['tuesday']['start'] != setting.tuesday_start or previous_timings['tuesday']['end'] != setting.tuesday_end:
            self.request.user.doctor.cancel_appointment_due_to_time_changed(1)
        elif previous_timings['wednesday']['start'] != setting.wednesday_start or previous_timings['wednesday']['end'] != setting.wednesday_end:
            self.request.user.doctor.cancel_appointment_due_to_time_changed(2)
        elif previous_timings['thursday']['start'] != setting.thursday_start or previous_timings['thursday']['end'] != setting.thursday_end:
            self.request.user.doctor.cancel_appointment_due_to_time_changed(3)
        elif previous_timings['friday']['start'] != setting.friday_start or previous_timings['friday']['end'] != setting.friday_end:
            self.request.user.doctor.cancel_appointment_due_to_time_changed(4)
        elif previous_timings['saturday']['start'] != setting.saturday_start or previous_timings['saturday']['end'] != setting.saturday_end:
            self.request.user.doctor.cancel_appointment_due_to_time_changed(5)
        elif previous_timings['sunday']['start'] != setting.sunday_start or previous_timings['sunday']['end'] != setting.sunday_end:
            self.request.user.doctor.cancel_appointment_due_to_time_changed(6)

        return HttpResponseRedirect(reverse('portal:profile'))
