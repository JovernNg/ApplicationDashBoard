from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from operations.models import (
    Application,
    Incident,
)

from operations.services.sla import (
    AT_RISK,
    BREACHED,
    WITHIN_SLA,
    calculate_sla_deadline,
    calculate_sla_progress,
    calculate_sla_status,
)


class SLATests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="tester",
            password="TestPassword123!",
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

        self.base_time = (
            timezone.now()
            .replace(
                microsecond=0
            )
        )

    def create_incident(
        self,
        priority,
    ):

        incident = (
            Incident.objects.create(
                application=self.application,
                title="SLA Test Incident",
                description="Testing SLA.",
                priority=priority,
                reported_by=self.user,
            )
        )

        Incident.objects.filter(
            pk=incident.pk
        ).update(
            reported_at=self.base_time
        )

        incident.refresh_from_db()

        return incident

    def test_critical_sla_is_two_hours(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.CRITICAL
        )

        deadline = (
            calculate_sla_deadline(
                incident
            )
        )

        self.assertEqual(
            deadline,
            (
                self.base_time
                + timedelta(hours=2)
            ),
        )

    def test_high_sla_is_four_hours(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.HIGH
        )

        deadline = (
            calculate_sla_deadline(
                incident
            )
        )

        self.assertEqual(
            deadline,
            (
                self.base_time
                + timedelta(hours=4)
            ),
        )

    def test_medium_sla_is_eight_hours(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.MEDIUM
        )

        deadline = (
            calculate_sla_deadline(
                incident
            )
        )

        self.assertEqual(
            deadline,
            (
                self.base_time
                + timedelta(hours=8)
            ),
        )

    def test_low_sla_is_twenty_four_hours(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.LOW
        )

        deadline = (
            calculate_sla_deadline(
                incident
            )
        )

        self.assertEqual(
            deadline,
            (
                self.base_time
                + timedelta(hours=24)
            ),
        )

    def test_incident_before_75_percent_is_within_sla(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.CRITICAL
        )

        current_time = (
            self.base_time
            + timedelta(hours=1)
        )

        status = calculate_sla_status(
            incident,
            current_time=current_time,
        )

        self.assertEqual(
            status,
            WITHIN_SLA,
        )

    def test_exactly_75_percent_is_at_risk(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.CRITICAL
        )

        current_time = (
            self.base_time
            + timedelta(
                hours=1,
                minutes=30,
            )
        )

        status = calculate_sla_status(
            incident,
            current_time=current_time,
        )

        self.assertEqual(
            status,
            AT_RISK,
        )

        progress = (
            calculate_sla_progress(
                incident,
                current_time=current_time,
            )
        )

        self.assertEqual(
            progress,
            75.0,
        )

    def test_after_75_percent_is_at_risk(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.CRITICAL
        )

        current_time = (
            self.base_time
            + timedelta(
                hours=1,
                minutes=59,
            )
        )

        status = calculate_sla_status(
            incident,
            current_time=current_time,
        )

        self.assertEqual(
            status,
            AT_RISK,
        )

    def test_exact_deadline_is_breached(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.CRITICAL
        )

        current_time = (
            self.base_time
            + timedelta(hours=2)
        )

        status = calculate_sla_status(
            incident,
            current_time=current_time,
        )

        self.assertEqual(
            status,
            BREACHED,
        )

    def test_sla_clock_stops_when_resolved(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.CRITICAL
        )

        incident.resolved_at = (
            self.base_time
            + timedelta(hours=1)
        )

        incident.save(
            update_fields=[
                "resolved_at",
            ]
        )

        much_later = (
            self.base_time
            + timedelta(hours=10)
        )

        status = calculate_sla_status(
            incident,
            current_time=much_later,
        )

        self.assertEqual(
            status,
            WITHIN_SLA,
        )

        progress = (
            calculate_sla_progress(
                incident,
                current_time=much_later,
            )
        )

        self.assertEqual(
            progress,
            50.0,
        )

    def test_resolution_at_deadline_is_breached(
        self
    ):

        incident = self.create_incident(
            Incident.Priority.CRITICAL
        )

        incident.resolved_at = (
            self.base_time
            + timedelta(hours=2)
        )

        incident.save(
            update_fields=[
                "resolved_at",
            ]
        )

        status = calculate_sla_status(
            incident,
            current_time=(
                self.base_time
                + timedelta(hours=10)
            ),
        )

        self.assertEqual(
            status,
            BREACHED,
        )