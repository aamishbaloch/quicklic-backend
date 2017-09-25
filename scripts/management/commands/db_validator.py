from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from entities.profile_item.models import DoctorProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Validate DB data."

    def handle(self, *args, **options):

        self.stdout.write("Checking Doctors Data")
        doctors = User.objects.filter(role=User.Role.DOCTOR)
        for doctor in doctors:
            try:
                DoctorProfile.objects.get(doctor=doctor)
            except DoctorProfile.DoesNotExist:
                self.stdout.write("Doctor {} {}: Profile not exists".format(doctor.first_name, doctor.last_name))

        self.stdout.write("Task Successful")
