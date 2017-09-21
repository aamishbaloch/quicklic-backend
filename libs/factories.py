import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'
    email = 'john.doe@gmail.com'
    password = factory.PostGenerationMethodCall('set_password', 'githubisawesome')
    role = User.Role.PATIENT
