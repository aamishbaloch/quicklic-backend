from django.forms.models import ModelForm
from entities.contact.models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'subject', 'message']


