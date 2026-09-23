from datetime import timedelta

from django.contrib.auth.models import (
    User,
)
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from operations.models import (
    Application,
    Incident,
)


class DashboardTests(TestCase):

    def setUp(self):

        self.user = (
            User.objects.create_user(
                username="dashboarduser",
                password="TestPassword123!",
            )
        )

        self.healthy = (
            Application.objects.create(
                name="Healthy App",
                owner="Operations",
                environment="Production",
                status=(
                    Application.Status.HEALTHY
                ),
                availability_percentage=100,
            )
        )

        self.degraded = (
            Application.objects.create(
                name="Degraded App",
                owner="Operations",
                environment="Production",
                status=(
                    Application.Status.DEGRADED
                ),
                availability_percentage=99,
            )
        )

        self.down = (
            Application.objects.create(
                name="Down App",
                owner="Operations",
                environment="Production",
                status=(
                    Application.Status.DOWN
                ),
                availability_percentage=95,
            )
        )

        self.maintenance = (
            Application.objects.create(
                name="Maintenance App",
                owner="Operations",
                environment="Production",
                status=(
                    Application.Status.MAINTENANCE
                ),
                availability_percentage=100,
            )
        )

        self.critical_incident = (
            Incident.objects.create(
                application=self.down,
                title="Critical outage",
                description="Critical test.",
                priority=(
                    Incident.Priority.CRITICAL
                ),
                status=(
                    Incident.Status.NEW
                ),
                reported_by=self.user,
            )
        )

        old_time = (
            timezone.now()
            - timedelta(hours=3)
        )

        Incident.objects.filter(
            pk=self.critical_incident.pk
        ).update(
            reported_at=old_time
        )

        self.critical_incident.refresh_from_db()

        self.high_incident = (
            Incident.objects.create(
                application=self.degraded,
                title="High priority issue",
                description="High test.",
                priority=(
                    Incident.Priority.HIGH
                ),
                status=(
                    Incident.Status.IN_PROGRESS
                ),
                reported_by=self.user,
            )
        )

        self.resolved_incident = (
            Incident.objects.create(
                application=self.healthy,
                title="Resolved issue",
                description="Resolved test.",
                priority=(
                    Incident.Priority.MEDIUM
                ),
                status=(
                    Incident.Status.RESOLVED
                ),
                reported_by=self.user,
                resolved_at=timezone.now(),
            )
        )

        self.closed_incident = (
            Incident.objects.create(
                application=self.healthy,
                title="Closed issue",
                description="Closed test.",
                priority=(
                    Incident.Priority.LOW
                ),
                status=(
                    Incident.Status.CLOSED
                ),
                reported_by=self.user,
                resolved_at=timezone.now(),
                closed_at=timezone.now(),
            )
        )

    def login(self):

        self.client.login(
            username="dashboarduser",
            password="TestPassword123!",
        )

    def test_dashboard_requires_login(
        self
    ):

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_application_counts(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.context[
                "total_applications"
            ],
            4,
        )

        self.assertEqual(
            response.context[
                "healthy_applications"
            ],
            1,
        )

        self.assertEqual(
            response.context[
                "problem_applications"
            ],
            2,
        )

    def test_open_incident_count(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.context[
                "open_incident_count"
            ],
            2,
        )

    def test_critical_incident_count(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.context[
                "critical_incident_count"
            ],
            1,
        )

    def test_sla_breach_count(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.context[
                "sla_breach_count"
            ],
            1,
        )

    def test_recent_incidents_are_displayed(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertContains(
            response,
            "Critical outage",
        )

        self.assertContains(
            response,
            "High priority issue",
        )

    def test_chart_data_is_correct(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.context[
                "application_status_data"
            ],
            [
                1,
                1,
                1,
                1,
            ],
        )

        self.assertEqual(
            response.context[
                "incident_priority_data"
            ],
            [
                1,
                1,
                0,
                0,
            ],
        )