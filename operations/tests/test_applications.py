from django.contrib.auth.models import (
    Group,
    User,
)
from django.test import TestCase
from django.urls import reverse

from operations.models import Application


class ApplicationTests(TestCase):

    def setUp(self):

        self.admin_group = Group.objects.create(
            name="Administrator"
        )

        self.operations_group = Group.objects.create(
            name="Operations User"
        )

        self.admin = User.objects.create_user(
            username="adminuser",
            password="TestPassword123!",
        )

        self.admin.groups.add(
            self.admin_group
        )

        self.operator = User.objects.create_user(
            username="operator1",
            password="TestPassword123!",
        )

        self.operator.groups.add(
            self.operations_group
        )

        self.application = Application.objects.create(
            name="Payment Portal",
            description="Test application",
            owner="Finance",
            environment="Production",
            support_contact="support@example.com",
            status=Application.Status.HEALTHY,
            availability_percentage=100,
        )

    def test_operator_can_view_application_list(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse("application_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Payment Portal",
        )

    def test_admin_can_create_application(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("application_create"),
            {
                "name": "HR Portal",
                "description": "Employee application",
                "owner": "Human Resources",
                "environment": "Production",
                "support_contact": "hr@example.com",
                "status": Application.Status.HEALTHY,
                "availability_percentage": "100.00",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            Application.objects.filter(
                name="HR Portal"
            ).exists()
        )

    def test_operator_cannot_create_application(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("application_create"),
            {
                "name": "Unauthorised App",
                "description": "Should not be created",
                "owner": "Test",
                "environment": "Production",
                "support_contact": "test@example.com",
                "status": Application.Status.HEALTHY,
                "availability_percentage": "100",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            Application.objects.filter(
                name="Unauthorised App"
            ).exists()
        )

    def test_admin_can_edit_application(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "application_edit",
                args=[
                    self.application.pk
                ],
            ),
            {
                "name": "Payment Portal",
                "description": "Updated",
                "owner": "Finance",
                "environment": "Production",
                "support_contact": "support@example.com",
                "status": Application.Status.DEGRADED,
                "availability_percentage": "99.50",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.application.refresh_from_db()

        self.assertEqual(
            self.application.status,
            Application.Status.DEGRADED,
        )

        self.assertEqual(
            self.application.description,
            "Updated",
        )

    def test_operator_cannot_edit_application(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "application_edit",
                args=[
                    self.application.pk
                ],
            ),
            {
                "name": "Changed by operator",
                "description": "Unauthorised change",
                "owner": "Test",
                "environment": "Production",
                "support_contact": "test@example.com",
                "status": Application.Status.DOWN,
                "availability_percentage": "50",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.application.refresh_from_db()

        self.assertEqual(
            self.application.name,
            "Payment Portal",
        )

        self.assertEqual(
            self.application.status,
            Application.Status.HEALTHY,
        )

    def test_availability_over_100_is_rejected(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("application_create"),
            {
                "name": "Invalid Application",
                "description": "Invalid availability test",
                "owner": "Test",
                "environment": "Production",
                "support_contact": "test@example.com",
                "status": Application.Status.HEALTHY,
                "availability_percentage": "110",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            Application.objects.filter(
                name="Invalid Application"
            ).exists()
        )