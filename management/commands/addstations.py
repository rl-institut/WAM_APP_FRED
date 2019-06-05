from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils import timezone

from ...models import WeatherStation

class Command(BaseCommand):

    def handle(self, *args, **options):

        positions = [Point(53.46, 9.65), Point(53.48, 9.53)]

        for i, pos in enumerate(positions):

            WeatherStation(wmoid=i, name='Station_{}'.format(i), geom=pos).save()

        print(WeatherStation.objects.all())
