from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class City(models.Model):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class Clinic(models.Model):
    code = models.CharField(_('code'), max_length=6, db_index=True, unique=True)
    name = models.CharField(_('name'), max_length=255, db_index=True)
    phone = models.CharField(_('phone'), max_length=255)
    email = models.EmailField(_('email'), blank=True, null=True)
    website = models.URLField(_('website'), blank=True, null=True)
    location = models.CharField(_('location'), max_length=255)
    city = models.ForeignKey(City, related_name="city")
    country = models.ForeignKey(Country, related_name="country")
    image = models.ImageField(upload_to='uploads/clinics/')
    image_thumb = models.ImageField(upload_to='uploads/clinics/thumbs/', blank=True, null=True)
    is_lab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def calculate_rating(self):
        rating = self.reviews.aggregate(Avg('rating'))
        self.rating = rating['rating__avg']
        self.save(update_fields=["rating"])

    def create_thumbnail(self):
        if not self.image:
            return

        if not hasattr(self.avatar.file, "content_type"):
            return

        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (200, 200)

        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(BytesIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
        self.image_thumb.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        return super(Clinic, self).save(*args, **kwargs)
