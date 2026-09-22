from django.contrib.auth.models import (
    Group,
    User,
)
from django.test import TestCase
from django.urls import reverse

from operations.models import (
    Application,
    AuditLog,
)


class AuditLogTests(TestCase):

    def setUp(self):

        admin_group = Group.objects.create(
            name="Administrator"
        )

        operations_group = (
            Group.objects.create(
                name="Operations User"
            )
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

        self.application = (
            Application.objects.create(
                name="Payment Portal",
                description="Test application",
                owner="Finance",
                environment="Production",
                support_contact=(
                    "support@example.com"
                ),
                status=(
                    Application.Status.HEALTHY
                ),
                availability_percentage=100,
            )
        )


    def test_application_creation_is_logged(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        self.client.post(
            reverse(
                "application_create"
            ),
            {
                "name":
                    "New Application",

                "description":
                    "New test application",

                "owner":
                    "Operations",

                "environment":
                    "Production",

                "support_contact":
                    "ops@example.com",

                "status":
                    Application.Status.HEALTHY,

                "availability_percentage":
                    "100",
            },
        )

        audit_log = (
            AuditLog.objects.get(
                action=(
                    AuditLog.Action
                    .APPLICATION_CREATED
                )
            )
        )

        self.assertEqual(
            audit_log.user,
            self.admin,
        )

        self.assertEqual(
            audit_log.application.name,
            "New Application",
        )


    def test_application_update_is_logged(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        self.client.post(
            reverse(
                "application_edit",
                args=[
                    self.application.pk
                ],
            ),
            {
                "name":
                    "Payment Portal",

                "description":
                    "Test application",

                "owner":
                    "Platform Operations",

                "environment":
                    "Production",

                "support_contact":
                    "support@example.com",

                "status":
                    Application.Status.HEALTHY,

                "availability_percentage":
                    "100",
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                action=(
                    AuditLog.Action
                    .APPLICATION_UPDATED
                ),
                application=self.application,
            ).exists()
        )


    def test_status_change_is_logged(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        self.client.post(
            reverse(
                "application_edit",
                args=[
                    self.application.pk
                ],
            ),
            {
                "name":
                    "Payment Portal",

                "description":
                    "Test application",

                "owner":
                    "Finance",

                "environment":
                    "Production",

                "support_contact":
                    "support@example.com",

                "status":
                    Application.Status.DEGRADED,

                "availability_percentage":
                    "100",
            },
        )

        audit_log = (
            AuditLog.objects.get(
                action=(
                    AuditLog.Action
                    .APPLICATION_STATUS_CHANGED
                )
            )
        )

        self.assertIn(
            "Healthy",
            audit_log.details,
        )

        self.assertIn(
            "Degraded",
            audit_log.details,
        )


    def test_admin_can_view_audit_log(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse(
                "audit_log_list"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_operator_cannot_view_audit_log(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse(
                "audit_log_list"
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )