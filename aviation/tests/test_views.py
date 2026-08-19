from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from aviation.models import Airport, City, Country


AIRPORT_URL = reverse("aviation:airport-list")


class AirportApiTests(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine")
        self.city = City.objects.create(name="Kyiv", country=self.country)
        self.airport = Airport.objects.create(
            name="Boryspil", closest_big_city="Kyiv", city=self.city
        )

        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="password123"
        )

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_user_can_list_airports(self):
        self.client.force_authenticate(self.user)
        res = self.client.get(AIRPORT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"][0]["name"], self.airport.name)

    def test_auth_user_cannot_create_airport(self):
        self.client.force_authenticate(self.user)
        payload = {
            "name": "New Airport",
            "closest_big_city": "Odessa",
            "city": self.city.id
        }
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_airport(self):
        self.client.force_authenticate(self.admin)
        payload = {
            "name": "New Airport",
            "closest_big_city": "Odessa",
            "city": self.city.id
        }
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
