from django.contrib.auth.models import User
from django.core.management import BaseCommand


class SeedsConstants:
    SUPERUSER_USERNAME = 'admin'
    SUPERUSER_PASSWORD = 'arbisoft'
    SUPERUSER_EMAIL = 'admin@example.com'


class Command(BaseCommand):
    help = "Add mandatory data."

    def handle(self, *args, **options):
        User.objects.create_superuser(
            username=SeedsConstants.SUPERUSER_USERNAME,
            password=SeedsConstants.SUPERUSER_PASSWORD,
            email=SeedsConstants.SUPERUSER_EMAIL
        )
        self.stdout.write("Super User created successfully...")

        self.stdout.write("Task Successful")
