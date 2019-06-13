import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User

class RegisterUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_payload = {
            "username": "testuser3",
            "password": "qwer1234",
            "email": "testuser4@test.com"
        }

    def test_register_user(self):

        res = self.client.post(
            path=reverse('register_user'),
            data=json.dumps(self.user_payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="testuser3")

        self.assertEqual(user.username, "testuser3")

class LoginUserTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user_payload = {
            "username": "testuser4",
            "password": "qwer1234",
            "email": "testuser4@test.com"
        }

        self.correct_login_payload = {
            "username": "testuser4",
            "password": "qwer1234"
        }

        self.incorrect_login_payload = {
            "username": "testuser4",
            "password": "121231"
        }

        self.user = User.objects.create_user(
            username=self.user_payload["username"],
            email=self.user_payload["email"],
            password=self.user_payload["password"]
        )

    def test_correct_login(self):

        login_res = self.client.post(
            path=reverse('login_user'),
            data=json.dumps(self.correct_login_payload),
            content_type='application/json'
        )

        self.assertEqual(login_res.status_code, status.HTTP_200_OK)

        json_res = json.loads(login_res.content)
        self.assertIn("token", json_res)

    def test_incorrect_login(self):

        login_res = self.client.post(
            path=reverse('login_user'),
            data=json.dumps(self.incorrect_login_payload),
            content_type='application/json'
        )

        self.assertEqual(login_res.status_code, status.HTTP_400_BAD_REQUEST)


