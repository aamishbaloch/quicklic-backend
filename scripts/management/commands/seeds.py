from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class SeedsConstants:
    pass


class Command(BaseCommand):
    help = "Add mandatory data."

    def handle(self, *args, **options):

        self.stdout.write("Task Successful")
