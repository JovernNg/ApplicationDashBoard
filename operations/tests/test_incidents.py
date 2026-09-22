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
)


class IncidentTests(TestCase):

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
            description="Payment system",
            owner="Finance",
            environment="Production",
            support_contact="support@example.com",
            status=Application.Status.HEALTHY,
            availability_percentage=100,
        )

    def test_incident_number_is_generated(
        self
    ):

        incident = Incident.objects.create(
            application=self.application,
            title="Payment Failure",
            description="Payment failed.",
            priority=Incident.Priority.CRITICAL,
            reported_by=self.admin,
        )

        self.assertTrue(
            incident.incident_number.startswith(
                "INC-"
            )
        )

        self.assertIn(
            str(incident.pk).zfill(4),
            incident.incident_number,
        )

    def test_new_incident_defaults_to_new_status(
        self
    ):

        incident = Incident.objects.create(
            application=self.application,
            title="Payment Failure",
            description="Payment failed.",
            priority=Incident.Priority.HIGH,
            reported_by=self.admin,
        )

        self.assertEqual(
            incident.status,
            Incident.Status.NEW,
        )

    def test_admin_can_create_incident(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("incident_create"),
            {
                "application":
                    self.application.pk,

                "title":
                    "Payment Failure",

                "description":
                    "Payment failed.",

                "priority":
                    Incident.Priority.CRITICAL,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            Incident.objects.filter(
                title="Payment Failure"
            ).exists()
        )

    def test_operator_can_create_incident(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("incident_create"),
            {
                "application":
                    self.application.pk,

                "title":
                    "Slow Response",

                "description":
                    "Application is slow.",

                "priority":
                    Incident.Priority.MEDIUM,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        incident = Incident.objects.get(
            title="Slow Response"
        )

        self.assertEqual(
            incident.reported_by,
            self.operator,
        )

    def test_logged_out_user_cannot_create_incident(
        self
    ):

        response = self.client.get(
            reverse("incident_create")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_authenticated_user_can_view_incident_list(
        self
    ):

        Incident.objects.create(
            application=self.application,
            title="Payment Failure",
            description="Payment failed.",
            priority=Incident.Priority.HIGH,
            reported_by=self.admin,
        )

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse("incident_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Payment Failure",
        )

    def test_incident_creation_is_audited(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        self.client.post(
            reverse("incident_create"),
            {
                "application":
                    self.application.pk,

                "title":
                    "Service Failure",

                "description":
                    "Service unavailable.",

                "priority":
                    Incident.Priority.CRITICAL,
            },
        )

        incident = Incident.objects.get(
            title="Service Failure"
        )

        self.assertTrue(
            AuditLog.objects.filter(
                action=(
                    AuditLog.Action
                    .INCIDENT_CREATED
                ),
                incident=incident,
                user=self.admin,
            ).exists()
        )