from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    title = models.CharField(_('title'), max_length=255)
    image = models.ImageField(upload_to='media/author/')
    facebook_url = models.CharField(_('facebook'), max_length=255)
    twitter_url = models.CharField(_('twitter'), max_length=255)
    instagram_url = models.CharField(_('instagram'), max_length=255)
    linkedin_url = models.CharField(_('linkedin'), max_length=255)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(Author, related_name="author")
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('message'))
    image = models.ImageField(upload_to='media/uploads/blogs/')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


