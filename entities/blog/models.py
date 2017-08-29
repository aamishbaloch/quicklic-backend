from django.db import models
from django.utils.translation import ugettext_lazy as _


class Blog(models.Model):
    author = models.CharField(_('name'), max_length=50, db_index=True)
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('message'))
    image = models.ImageField(upload_to = 'media/blogs/')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
