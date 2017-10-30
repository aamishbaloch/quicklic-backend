from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from entities.blog.models import Blog
from website import constants
from website.forms import ContactForm
from django.contrib import messages


class LoginView(TemplateView):
    template_name = "portal/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context
