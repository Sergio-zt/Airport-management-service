from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from aviation.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    City,
    Country
)
from orders.models import Order, Ticket


ORDER_URL = reverse("orders:order-list")


class OrderApiTests(APITestCase):
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            email="client@test.com", password="password123"
        )
        self.client.force_authenticate(self.user)

        self.country = Country.objects.create(name="Test Country")
        self.city = City.objects.create(name="Test City", country=self.country)

        self.airport1 = Airport.objects.create(
            name="Airport A", closest_big_city="City A", city=self.city
        )
        self.airport2 = Airport.objects.create(
            name="Airport B", closest_big_city="City B", city=self.city
        )

        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=500
        )

        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="Boeing", rows=10, seats_in_row=6, airplane_type=self.airplane_type
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2026-12-01T10:00:00Z",
            arrival_time="2026-12-01T12:00:00Z",
        )

    def test_create_order_with_tickets(self):
        payload = {
            "tickets": [
                {"row": 1, "seat": 1, "flight": self.flight.id},
                {"row": 1, "seat": 2, "flight": self.flight.id},
            ]
        }
        res = self.client.post(ORDER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Ticket.objects.filter(order__user=self.user).count(), 2)

    def test_unauthenticated_user_cannot_create_order(self):
        self.client.logout()
        payload = {
            "tickets": [{"row": 1, "seat": 1, "flight": self.flight.id}]
        }
        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
