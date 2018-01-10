import datetime
from datetime import timedelta
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from entities.clinic.models import Country, City, Clinic
from entities.resources.models import Service, Specialization, Occupation
from libs.managers import QueryManager
from libs.utils import get_verification_code, next_weekday, get_start_datetime_from_date_string, \
    get_end_datetime_from_date_string
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
        ADMIN = 3

        Choices = (
            (DOCTOR, 'Doctor'),
            (PATIENT, 'Patient'),
            (ADMIN, 'ADMIN'),
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

    device_id = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.IntegerField(blank=True, null=True)

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

    def update_device_information(self, device_id, device_type):
        self.device_type = device_type
        self.device_id = device_id
        self.save()

    def is_doctor(self):
        return hasattr(self, 'doctor')

    def is_patient(self):
        return hasattr(self, 'patient')

    def is_admin(self):
        return hasattr(self, 'moderator')

    @staticmethod
    def is_exists(phone):
        user = User.objects.filter(phone=phone).first()
        if user:
            return True
        return False

    @property
    def get_avatar(self):
        if self.avatar:
            return "{}{}{}".format(MEDIA_ROOT, MEDIA_URL, self.avatar.url)


class Moderator(User):
    role = models.IntegerField(default=User.Role.ADMIN)


class Doctor(User):
    role = models.IntegerField(default=User.Role.DOCTOR)
    services = models.ManyToManyField(Service, related_name="doctor")
    specialization = models.ForeignKey(Specialization, related_name="doctor", blank=True, null=True)
    degree = models.CharField(_('degree'), max_length=50, blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2)

    def calculate_rating(self):
        rating = self.reviews.aggregate(Avg('rating'))
        self.rating = rating['rating__avg']
        self.save(update_fields=["rating"])

    def cancel_appointment_due_to_time_changed(self, day_number):
        """
        MONDAY 0, TUESDAY 1, WEDNESDAY 2, THURSDAY 3, FRIDAY 4, SATURDAY 5, SUNDAY 6
        """
        from libs.quicklic_utils import cancel_appointments_of_day_and_send_notify

        current = datetime.datetime.now()
        limit = current + timedelta(30)
        date_to_cancel = next_weekday(current, day_number)

        while date_to_cancel <= limit:
            cancel_appointments_of_day_and_send_notify(date_to_cancel)
            date_to_cancel = next_weekday(date_to_cancel, day_number)


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

    def get_day_timings(self, day_number):
        """
        method will return day timings by getting a number

        MONDAY 0, TUESDAY 1, WEDNESDAY 2, THURSDAY 3, FRIDAY 4, SATURDAY 5, SUNDAY 6
        """

        if day_number == 0:
            return self.monday_start, self.monday_end
        elif day_number == 1:
            return self.tuesday_start, self.tuesday_end
        elif day_number == 2:
            return self.wednesday_start, self.wednesday_end
        elif day_number == 3:
            return self.thursday_start, self.thursday_end
        elif day_number == 4:
            return self.friday_start, self.friday_end
        elif day_number == 5:
            return self.saturday_start, self.saturday_end
        elif day_number == 6:
            return self.sunday_start, self.sunday_end

    def get_timings_with_switch(self):
        return {
            "monday": {
                "switch": True if self.monday_start and self.monday_end else False,
                "start": "{:02d}:{:02d}".format(self.monday_start.hour, self.monday_start.minute) if self.monday_start else "00:00",
                "end": "{:02d}:{:02d}".format(self.monday_end.hour, self.monday_end.minute) if self.monday_end else "00:00",
            },
            "tuesday": {
                "switch": True if self.tuesday_start and self.tuesday_end else False,
                "start": "{:02d}:{:02d}".format(self.tuesday_start.hour, self.tuesday_start.minute) if self.tuesday_start else "00:00",
                "end": "{:02d}:{:02d}".format(self.tuesday_end.hour, self.tuesday_end.minute) if self.tuesday_end else "00:00",
            },
            "wednesday": {
                "switch": True if self.wednesday_start and self.wednesday_end else False,
                "start": "{:02d}:{:02d}".format(self.wednesday_start.hour, self.wednesday_start.minute) if self.wednesday_start else "00:00",
                "end": "{:02d}:{:02d}".format(self.wednesday_end.hour, self.wednesday_end.minute) if self.wednesday_end else "00:00",
            },
            "thursday": {
                "switch": True if self.thursday_start and self.thursday_end else False,
                "start": "{:02d}:{:02d}".format(self.thursday_start.hour, self.thursday_start.minute) if self.thursday_start else "00:00",
                "end": "{:02d}:{:02d}".format(self.thursday_end.hour, self.thursday_end.minute) if self.thursday_end else "00:00",
            },
            "friday": {
                "switch": True if self.friday_start and self.friday_end else False,
                "start": "{:02d}:{:02d}".format(self.friday_start.hour, self.friday_start.minute) if self.friday_start else "00:00",
                "end": "{:02d}:{:02d}".format(self.friday_end.hour, self.friday_end.minute) if self.friday_end else "00:00",
            },
            "saturday": {
                "switch": True if self.saturday_start and self.saturday_end else False,
                "start": "{:02d}:{:02d}".format(self.saturday_start.hour, self.saturday_start.minute) if self.saturday_start else "00:00",
                "end": "{:02d}:{:02d}".format(self.saturday_end.hour, self.saturday_end.minute) if self.saturday_end else "00:00",
            },
            "sunday": {
                "switch": True if self.sunday_start and self.sunday_end else False,
                "start": "{:02d}:{:02d}".format(self.sunday_start.hour, self.sunday_start.minute) if self.sunday_start else "00:00",
                "end": "{:02d}:{:02d}".format(self.sunday_end.hour, self.sunday_end.minute) if self.sunday_end else "00:00",
            }
        }

    def get_timings_list(self):
        return [
            {
                "day": "Monday",
                "start": self.monday_start,
                "end": self.monday_end,
            },
            {
                "day": "Tuesday",
                "start": self.tuesday_start,
                "end": self.tuesday_end,
            },
            {
                "day": "Wednesday",
                "start": self.wednesday_start,
                "end": self.wednesday_end,
            },
            {
                "day": "Thursday",
                "start": self.thursday_start,
                "end": self.thursday_end,
            },
            {
                "day": "Friday",
                "start": self.friday_start,
                "end": self.friday_end,
            },
            {
                "day": "Saturday",
                "start": self.saturday_start,
                "end": self.saturday_end,
            },
            {
                "day": "Sunday",
                "start": self.sunday_start,
                "end": self.sunday_end,
            },

        ]


@receiver(post_save, sender=Doctor)
def doctor_post_save_callback(sender, **kwargs):
    """
    settings to be created after doctor's creation
    """
    doctor = kwargs['instance']
    if not hasattr(doctor, 'setting'):
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
        if hasattr(user, "verification_code"):
            user.verification_code.code = get_verification_code()
            user.verification_code.save()
            return user.verification_code
        else:
            verification_code = VerificationCode.objects.create(user=user, code=get_verification_code())
            return verification_code.code
