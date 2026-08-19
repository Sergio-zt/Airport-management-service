from django.test import TestCase
from aviation.models import Airport, City, Country


class AirportModelTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine")
        self.city = City.objects.create(name="Kyiv", country=self.country)
        self.airport = Airport.objects.create(
            name="Boryspil International Airport",
            closest_big_city="Kyiv",
            city=self.city
        )

    def test_airport_str_representation(self):
        expected_str = f"{self.airport.name} - {self.airport.closest_big_city}"
        self.assertEqual(str(self.airport), expected_str)

    def test_city_str_representation(self):
        expected_str = f"{self.city.name} ({self.country.name})"
        self.assertEqual(str(self.city), expected_str)
