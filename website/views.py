from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from website.forms import ContactForm


class HomeView(TemplateView):
    template_name = "website/main.html"


class ContactUsView(TemplateView):

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('website:home'))
        return HttpResponseRedirect(reverse('website:home'))
