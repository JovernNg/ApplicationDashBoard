from django.contrib.auth.models import (
    Group,
    User,
)
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from operations.models import (
    Application,
    AuditLog,
    Incident,
)


class WorkflowTests(TestCase):

    def setUp(self):

        admin_group = Group.objects.create(
            name="Administrator"
        )

        operations_group = Group.objects.create(
            name="Operations User"
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
                reported_by=self.admin,
            )
        )

    def test_admin_assignment_moves_incident_to_assigned(
        self
    ):

        self.client.login(
            username="adminuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_assign",
                args=[self.incident.pk],
            ),
            {
                "assigned_user":
                    self.operator1.pk,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.incident.refresh_from_db()

        self.assertEqual(
            self.incident.assigned_user,
            self.operator1,
        )

        self.assertEqual(
            self.incident.status,
            Incident.Status.ASSIGNED,
        )

    def test_operator_cannot_assign_incident(
        self
    ):

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.get(
            reverse(
                "incident_assign",
                args=[self.incident.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_assigned_operator_can_start_progress(
        self
    ):

        self.incident.assigned_user = (
            self.operator1
        )

        self.incident.status = (
            Incident.Status.ASSIGNED
        )

        self.incident.save()

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[self.incident.pk],
            ),
            {
                "new_status":
                    Incident.Status.IN_PROGRESS,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.incident.refresh_from_db()

        self.assertEqual(
            self.incident.status,
            Incident.Status.IN_PROGRESS,
        )

    def test_non_assigned_operator_cannot_transition(
        self
    ):

        self.incident.assigned_user = (
            self.operator1
        )

        self.incident.status = (
            Incident.Status.ASSIGNED
        )

        self.incident.save()

        self.client.login(
            username="operator2",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[self.incident.pk],
            ),
            {
                "new_status":
                    Incident.Status.IN_PROGRESS,
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_incident_cannot_skip_status(
        self
    ):

        self.incident.assigned_user = (
            self.operator1
        )

        self.incident.status = (
            Incident.Status.ASSIGNED
        )

        self.incident.save()

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[self.incident.pk],
            ),
            {
                "new_status":
                    Incident.Status.RESOLVED,

                "resolution_notes":
                    "Attempted skip.",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.incident.refresh_from_db()

        self.assertEqual(
            self.incident.status,
            Incident.Status.ASSIGNED,
        )

    def test_resolution_requires_notes(
        self
    ):

        self.incident.assigned_user = (
            self.operator1
        )

        self.incident.status = (
            Incident.Status.IN_PROGRESS
        )

        self.incident.save()

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[self.incident.pk],
            ),
            {
                "new_status":
                    Incident.Status.RESOLVED,

                "resolution_notes": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.incident.refresh_from_db()

        self.assertEqual(
            self.incident.status,
            Incident.Status.IN_PROGRESS,
        )

        self.assertIsNone(
            self.incident.resolved_at
        )

    def test_resolve_records_timestamp_and_notes(
        self
    ):

        self.incident.assigned_user = (
            self.operator1
        )

        self.incident.status = (
            Incident.Status.IN_PROGRESS
        )

        self.incident.save()

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[self.incident.pk],
            ),
            {
                "new_status":
                    Incident.Status.RESOLVED,

                "resolution_notes":
                    "Service restarted successfully.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.incident.refresh_from_db()

        self.assertEqual(
            self.incident.status,
            Incident.Status.RESOLVED,
        )

        self.assertIsNotNone(
            self.incident.resolved_at
        )

        self.assertEqual(
            self.incident.resolution_notes,
            "Service restarted successfully.",
        )

    def test_close_records_closed_timestamp(
        self
    ):

        self.incident.assigned_user = (
            self.operator1
        )

        self.incident.status = (
            Incident.Status.RESOLVED
        )

        self.incident.resolved_at = (
            timezone.now()
        )

        self.incident.resolution_notes = (
            "Resolved."
        )

        self.incident.save()

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[self.incident.pk],
            ),
            {
                "new_status":
                    Incident.Status.CLOSED,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.incident.refresh_from_db()

        self.assertEqual(
            self.incident.status,
            Incident.Status.CLOSED,
        )

        self.assertIsNotNone(
            self.incident.closed_at
        )

    def test_status_transition_is_audited(
        self
    ):

        self.incident.assigned_user = (
            self.operator1
        )

        self.incident.status = (
            Incident.Status.ASSIGNED
        )

        self.incident.save()

        self.client.login(
            username="operator1",
            password="TestPassword123!",
        )

        self.client.post(
            reverse(
                "incident_transition",
                args=[self.incident.pk],
            ),
            {
                "new_status":
                    Incident.Status.IN_PROGRESS,
            },
        )

        self.assertTrue(
            AuditLog.objects.filter(
                incident=self.incident,
                action=(
                    AuditLog.Action
                    .INCIDENT_STATUS_CHANGED
                ),
                user=self.operator1,
            ).exists()
        )