from django.test import TestCase
from aviation.models import Airport, City, Country
from aviation.serializers import AirportSerializer


class AirportSerializerTests(TestCase):
    def test_airport_serialization(self):
        country = Country.objects.create(name="Ukraine")
        city = City.objects.create(name="Lviv", country=country)
        airport = Airport.objects.create(
            name="Danylo Halytskyi Airport",
            closest_big_city="Lviv",
            city=city
        )

        serializer = AirportSerializer(airport)

        self.assertEqual(serializer.data["name"], "Danylo Halytskyi Airport")
        self.assertEqual(serializer.data["closest_big_city"], "Lviv")
        self.assertEqual(serializer.data["city"], city.id)
