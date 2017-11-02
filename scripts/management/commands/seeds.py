from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from entities.appointment.models import AppointmentReason
from entities.clinic.models import Country, City
from entities.resources.models import Service, Specialization, Occupation

from seeds.geographic_seeds import country_data
from seeds.medical_services_seeds import services_data
from seeds.medical_specialization_seeds import specializations_data
from seeds.occupation_seeds import occupations_data
from seeds.appointment_reason_seeds import appointment_reason_data

User = get_user_model()


class SeedsConstants:
    pass


class Command(BaseCommand):
    help = "Add mandatory data."

    def handle(self, *args, **options):
        self.stdout.write("Adding Geographical Details")
        for country_detail in country_data:
            country, created = Country.objects.get_or_create(name=country_detail["name"])
            if created:
                self.stdout.write("New Country Created: {}".format(country.name))
            for city_detail in country_detail["city_data"]:
                city, created = City.objects.get_or_create(name=city_detail["name"])
                if created:
                    self.stdout.write("New City Created in Country {}: {}".format(country.name, city.name))

        self.stdout.write("Adding Medical Details")
        for service_data in services_data:
            service, created = Service.objects.get_or_create(name=service_data)
            if created:
                self.stdout.write("New Service Created: {}".format(service.name))

        for specialization_data in specializations_data:
            specialization, created = Specialization.objects.get_or_create(name=specialization_data)
            if created:
                self.stdout.write("New Specialization Created: {}".format(specialization.name))

        for occupation_data in occupations_data:
            occupation, created = Occupation.objects.get_or_create(name=occupation_data)
            if created:
                self.stdout.write("New Occupation Created: {}".format(occupation.name))

        for appointment_reason in appointment_reason_data:
            reason, created = AppointmentReason.objects.get_or_create(name=appointment_reason)
            if created:
                self.stdout.write("New Appointment Reason Created: {}".format(reason.name))

        self.stdout.write("Task Successful")
