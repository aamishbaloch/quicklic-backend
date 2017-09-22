import factory
from django.contrib.auth import get_user_model
from factory import fuzzy

User = get_user_model()

FACTORY_USER_PASSWORD = 'githubisawesome'


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'
    email = factory.Sequence(lambda n: 'patient{0}@email.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', FACTORY_USER_PASSWORD)
    role = User.Role.PATIENT
    gender = User.Gender.MALE
    phone = "23423324234"
    dob = "2017-08-08"


class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'
    email = factory.Sequence(lambda n: 'doctor{0}@email.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', FACTORY_USER_PASSWORD)
    role = User.Role.DOCTOR
    gender = User.Gender.MALE
    phone = "23423324234"
    dob = "2017-08-08"


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'
    email = factory.Sequence(lambda n: 'admin{0}@email.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', FACTORY_USER_PASSWORD)
    role = User.Role.ADMIN
    gender = User.Gender.MALE
    phone = "23423324234"
    dob = "2017-08-08"
