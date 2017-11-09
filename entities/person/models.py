import datetime
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from entities.clinic.models import Country, City, Clinic
from entities.resources.models import Service, Specialization, Occupation
from libs.managers import QueryManager
from libs.utils import get_verification_code
from quicklic_backend.settings import MEDIA_URL, MEDIA_ROOT


class UserManager(BaseUserManager, QueryManager):
    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError('Phone is required')
        phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Role:
        DOCTOR = 1
        PATIENT = 2

        Choices = (
            (DOCTOR, 'Doctor'),
            (PATIENT, 'Patient'),
        )

    class Gender:
        UNKNOWN = 3
        MALE = 1
        FEMALE = 2

        Choices = (
            (UNKNOWN, 'Unknown'),
            (FEMALE, 'Female'),
            (MALE, 'Male')
        )

    email = models.EmailField(_('email address'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    joined_on = models.DateTimeField(_('date joined'), default=timezone.now,
                                     help_text=_('Designates when the user joined the system.'))

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into admin site.'))

    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='uploads/avatars/', null=True, blank=True)
    gender = models.IntegerField(_('gender'), choices=Gender.Choices, default=Gender.UNKNOWN)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=255, unique=True)
    dob = models.DateField(_('date of birth'), default=datetime.date.today)
    country = models.ForeignKey(Country, related_name="user", blank=True, null=True)
    city = models.ForeignKey(City, related_name="user", blank=True, null=True)
    clinic = models.ManyToManyField(Clinic, related_name="user", blank=True)
    verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
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

    def status(self):
        if self.is_active:
            return "ACTIVE"
        else:
            return "BLOCKED"

    def get_gender(self):
        for choice in User.Gender.Choices:
            if choice[0] == self.gender:
                return choice[1]

    @property
    def get_avatar(self):
        if self.avatar:
            return "{}{}{}".format(MEDIA_ROOT, MEDIA_URL, self.avatar.url)


class Doctor(User):
    role = models.IntegerField(default=User.Role.DOCTOR)
    services = models.ManyToManyField(Service, related_name="doctor")
    specialization = models.ForeignKey(Specialization, related_name="doctor", blank=True, null=True)
    degree = models.CharField(_('degree'), max_length=50, blank=True, null=True)


class DoctorSetting(models.Model):
    physician = models.OneToOneField(Doctor, related_name='setting')
    slot_time = models.IntegerField(db_index=True, default=10)
    monday_start = models.TimeField(blank=True, null=True)
    monday_end = models.TimeField(blank=True, null=True)
    tuesday_start = models.TimeField(blank=True, null=True)
    tuesday_end = models.TimeField(blank=True, null=True)
    wednesday_start = models.TimeField(blank=True, null=True)
    wednesday_end = models.TimeField(blank=True, null=True)
    thursday_start = models.TimeField(blank=True, null=True)
    thursday_end = models.TimeField(blank=True, null=True)
    friday_start = models.TimeField(blank=True, null=True)
    friday_end = models.TimeField(blank=True, null=True)
    saturday_start = models.TimeField(blank=True, null=True)
    saturday_end = models.TimeField(blank=True, null=True)
    sunday_start = models.TimeField(blank=True, null=True)
    sunday_end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.physician.get_full_name()


@receiver(post_save, sender=Doctor)
def doctor_post_save_callback(sender, **kwargs):
    """
    settings to be created after doctor's creation
    """
    doctor = kwargs['instance']
    setting = DoctorSetting()
    setting.physician = doctor
    setting.save()


class Patient(User):

    class MaritalStatus:
        MARRIED = 1
        SINGLE = 2

        Choices = (
            (MARRIED, 'MARRIED'),
            (SINGLE, 'SINGLE'),
        )

    role = models.IntegerField(default=User.Role.PATIENT)
    height = models.FloatField(_('height'), blank=True, null=True)
    weight = models.FloatField(_('weight'), blank=True, null=True)
    occupation = models.ForeignKey(Occupation, related_name="patient", blank=True, null=True)
    marital_status = models.IntegerField(_('marital status'), choices=MaritalStatus.Choices, blank=True, null=True)


class VerificationCode(models.Model):
    user = models.OneToOneField(User, related_name="verification_code")
    code = models.CharField(max_length=6, db_index=True)

    def __str__(self):
        return self.user.get_full_name()

    @staticmethod
    def generate_code_for_user(user):
        verification_code = VerificationCode.objects.create(user=user, code=get_verification_code())
        return verification_code.code
