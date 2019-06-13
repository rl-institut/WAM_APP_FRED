from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from ...models import WeatherStation


class Command(BaseCommand):

    def handle(self, *args, **options):

        positions = [Point(9.65, 53.46), Point(9.53, 53.48)]

        for i, pos in enumerate(positions):

            WeatherStation(wmoid=i, name='Station_{}'.format(i), geom=pos).save()

        print(WeatherStation.objects.all())
