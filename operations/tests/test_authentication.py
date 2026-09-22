from django.contrib.auth.models import (
    User,
)
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):

    def setUp(self):

        self.user = (
            User.objects.create_user(
                username="operator1",
                password="TestPassword123!",
            )
        )


    def test_logged_out_user_redirected(
        self
    ):

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302,
        )


    def test_valid_login(self):

        result = self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        self.assertTrue(result)


    def test_invalid_login(self):

        result = self.client.login(
            username="operator1",
            password="wrong",
        )

        self.assertFalse(result)