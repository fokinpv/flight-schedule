import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User


# initialize the APIClient app
client = Client()

class RegisterUserTest(TestCase):

    def setUp(self):
        self.user_payload = {
            "username": "testuser3",
            "password": "qwer1234",
            "email": "testuser4@test.com"
        }

    def test_register_user(self):

        res = client.post(
            path=reverse('register_user'),
            data=json.dumps(self.user_payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="testuser3")

        self.assertEqual(user.username, "testuser3")