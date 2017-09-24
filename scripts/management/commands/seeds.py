from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from entities.clinic.models import Country, City

User = get_user_model()


class SeedsConstants:
    pass


class Command(BaseCommand):
    help = "Add mandatory data."

    def handle(self, *args, **options):
        country_data = [
            {
                "name": "Pakistan",
                "city_data": [
                    {
                        "name": "Lahore",
                    },
                    {
                        "name": "Islamabad",
                    }
                ]
            }
        ]

        for country_detail in country_data:
            Country.objects.create(name=country_detail["name"])
            for city_detail in country_detail["city_data"]:
                City.objects.create(name=city_detail["name"])

        self.stdout.write("Task Successful")
