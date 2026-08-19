from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


CREATE_USER_URL = reverse("users:create")


class UserApiTests(APITestCase):
    def test_create_user_success(self):
        payload = {
            "email": "testuser@test.com",
            "password": "testpassword123"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user)

        self.assertTrue(user.check_password(payload["password"]))
