from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from website import constants
from website.forms import ContactForm
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "website/main.html"


class ContactUsView(TemplateView):

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, constants.HELLO_MESSAGE)
            return HttpResponseRedirect(reverse('website:home'))

        messages.error(request, constants.OPERATION_UNSUCCESSFUL)
        return HttpResponseRedirect(reverse('website:home'))
