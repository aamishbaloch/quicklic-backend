from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from libs.managers import QueryManager


class UserManager(BaseUserManager, QueryManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', User.Role.QADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Gender:
        UNKNOWN = 3
        MALE = 1
        FEMALE = 2

        Choices = (
            (UNKNOWN, 'Unknown'),
            (FEMALE, 'Female'),
            (MALE, 'Male')
        )

    class Role:
        DOCTOR = 1
        PATIENT = 2
        ADMIN = 3
        QADMIN = 4

        Choices = (
            (DOCTOR, 'DOCTOR'),
            (PATIENT, 'PATIENT'),
            (ADMIN, 'ADMIN'),
            (QADMIN, 'QADMIN'),
        )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    joined_on = models.DateTimeField(_('date joined'), default=timezone.now,
                                     help_text=_('Designates when the user joined the system.'))

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into admin site.'))

    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='uploads/avatars/', null=True, blank=True)
    gender = models.IntegerField(_('gender'), choices=Gender.Choices, blank=True, default=Gender.UNKNOWN)
    role = models.IntegerField(_('role'), choices=Role.Choices)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=255)
    dob = models.DateField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)