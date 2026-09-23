from django.contrib.auth.models import (
    Group,
    User,
)
from django.test import TestCase
from django.urls import reverse

from operations.models import (
    Application,
    AuditLog,
    Incident,
    IncidentUpdate,
)


class IncidentUpdateTests(TestCase):

    def setUp(self):

        admin_group = Group.objects.create(
            name="Administrator"
        )

        operations_group = (
            Group.objects.create(
                name="Operations User"
            )
        )

        self.admin = User.objects.create_user(
            username="adminuser",
            password="TestPassword123!",
        )

        self.admin.groups.add(
            admin_group
        )

        self.operator1 = (
            User.objects.create_user(
                username="operator1",
                password="TestPassword123!",
            )
        )

        self.operator1.groups.add(
            operations_group
        )

        self.operator2 = (
            User.objects.create_user(
                username="operator2",
                password="TestPassword123!",
            )
        )

        self.operator2.groups.add(
            operations_group
        )

        self.application = (
            Application.objects.create(
                name="Payment Portal",
                description="Payment system",
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

        self.incident = (
            Incident.objects.create(
                application=self.application,
                title="Payment Failure",
                description="Payments failing.",
                priority=(
                    Incident.Priority.CRITICAL
                ),
                status=(
                    Incident.Status.ASSIGNED
                ),
                reported_by=self.admin,
                assigned_user=self.operator1,
            )
        )

    def test_assigned_operator_can_add_update(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_update_create",
                args=[self.incident.pk],
            ),
            {
                "update_text":
                    "Investigating logs.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            IncidentUpdate.objects.filter(
                incident=self.incident,
                user=self.operator1,
                update_text=(
                    "Investigating logs."
                ),
            ).exists()
        )

    def test_admin_can_add_update(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_update_create",
                args=[self.incident.pk],
            ),
            {
                "update_text":
                    "Administrator update.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            IncidentUpdate.objects.filter(
                user=self.admin,
            ).exists()
        )

    def test_unassigned_operator_cannot_add_update(
        self
    ):

        self.client.login(
            username="operator2",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_update_create",
                args=[self.incident.pk],
            ),
            {
                "update_text":
                    "Unauthorised update.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            IncidentUpdate.objects.filter(
                update_text=(
                    "Unauthorised update."
                )
            ).exists()
        )

    def test_logged_out_user_cannot_add_update(
        self
    ):

        response = self.client.get(
            reverse(
                "incident_update_create",
                args=[self.incident.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_empty_update_is_rejected(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_update_create",
                args=[self.incident.pk],
            ),
            {
                "update_text": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            IncidentUpdate.objects.count(),
            0,
        )

    def test_update_is_audited(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        self.client.post(
            reverse(
                "incident_update_create",
                args=[self.incident.pk],
            ),
            {
                "update_text":
                    "Checking service logs.",
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                incident=self.incident,
                user=self.operator1,
                action=(
                    AuditLog.Action
                    .INCIDENT_UPDATE_ADDED
                ),
            ).exists()
        )

    def test_incident_detail_displays_updates(
        self
    ):

        IncidentUpdate.objects.create(
            incident=self.incident,
            user=self.operator1,
            update_text=(
                "Timeline test update."
            ),
        )

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse(
                "incident_detail",
                args=[self.incident.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Timeline test update.",
        )

    def test_closed_incident_rejects_update(
        self
    ):

        self.incident.status = (
            Incident.Status.CLOSED
        )

        self.incident.save()

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_update_create",
                args=[self.incident.pk],
            ),
            {
                "update_text":
                    "Should not be added.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            IncidentUpdate.objects.filter(
                update_text=(
                    "Should not be added."
                )
            ).exists()
        )