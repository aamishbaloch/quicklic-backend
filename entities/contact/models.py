from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    phone = models.CharField(_('phone'), max_length=20, db_index=True)
    email = models.EmailField(_('email'), db_index=True)
    subject = models.CharField(_('subject'), max_length=255)
    message = models.TextField(_('message'))
    contacted = models.BooleanField(_('contacted'), db_index=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
