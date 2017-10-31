from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.base import View

from portal import constants
from portal.forms import LoginForm

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
                if not user.role == User.Role.PATIENT:
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

    def get_context_data(self, **kwargs):
        context = super(PortalHomeView, self).get_context_data(**kwargs)
        return context
