from django.core.management.base import BaseCommand
from ...models import WeatherStation


class Command(BaseCommand):

    def handle(self, *args, **options):
        WeatherStation.objects.all().delete()
