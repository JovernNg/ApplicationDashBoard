from django.contrib.auth.models import (
    Group,
    User,
)
from django.test import TestCase
from django.urls import reverse


class PermissionTests(TestCase):

    def setUp(self):

        admin_group = Group.objects.create(
            name="Administrator"
        )

        operations_group = Group.objects.create(
            name="Operations User"
        )


        self.admin = (
            User.objects.create_user(
                username="adminuser",
                password="TestPassword123!",
            )
        )

        self.admin.groups.add(
            admin_group
        )


        self.operator = (
            User.objects.create_user(
                username="operator1",
                password="TestPassword123!",
            )
        )

        self.operator.groups.add(
            operations_group
        )


    def test_admin_access_allowed(self):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse(
                "administrator_test"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_operator_access_denied(self):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse(
                "administrator_test"
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )