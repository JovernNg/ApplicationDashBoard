from django.contrib.auth.models import (
    User,
)
from django.test import TestCase
from django.urls import reverse

from operations.models import (
    Application,
    Incident,
)


class IncidentSearchFilterTests(
    TestCase
):

    def setUp(self):

        self.user = (
            User.objects.create_user(
                username="searchuser",
                password="TestPassword123!",
            )
        )

        self.operator1 = (
            User.objects.create_user(
                username="operator1",
                password="TestPassword123!",
            )
        )

        self.operator2 = (
            User.objects.create_user(
                username="operator2",
                password="TestPassword123!",
            )
        )


        self.payment_app = (
            Application.objects.create(
                name="Payment Portal",
                description="Payment system",
                owner="Finance",
                environment="Production",
                status=(
                    Application.Status.HEALTHY
                ),
            )
        )


        self.customer_app = (
            Application.objects.create(
                name="Customer Portal",
                description="Customer system",
                owner="Customer Services",
                environment="Production",
                status=(
                    Application.Status.DEGRADED
                ),
            )
        )


        self.incident1 = (
            Incident.objects.create(
                application=self.payment_app,
                title="Payment Gateway Failure",
                description=(
                    "External gateway "
                    "is unavailable."
                ),
                priority=(
                    Incident.Priority.CRITICAL
                ),
                status=(
                    Incident.Status.IN_PROGRESS
                ),
                reported_by=self.user,
                assigned_user=self.operator1,
            )
        )


        self.incident2 = (
            Incident.objects.create(
                application=self.customer_app,
                title="Customer Login Slow",
                description=(
                    "Login requests "
                    "are responding slowly."
                ),
                priority=(
                    Incident.Priority.HIGH
                ),
                status=(
                    Incident.Status.ASSIGNED
                ),
                reported_by=self.user,
                assigned_user=self.operator2,
            )
        )


        self.incident3 = (
            Incident.objects.create(
                application=self.payment_app,
                title="Payment Report Delay",
                description=(
                    "Scheduled report "
                    "processing is delayed."
                ),
                priority=(
                    Incident.Priority.MEDIUM
                ),
                status=(
                    Incident.Status.NEW
                ),
                reported_by=self.user,
            )
        )


    def login(self):

        self.client.login(
            username="searchuser",
            password="TestPassword123!",
        )


    def test_search_by_title(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "q": "gateway",
            },
        )

        self.assertIn(
            self.incident1,
            response.context[
                "incidents"
            ],
        )

        self.assertNotIn(
            self.incident2,
            response.context[
                "incidents"
            ],
        )


    def test_search_by_description(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "q": "responding slowly",
            },
        )

        self.assertIn(
            self.incident2,
            response.context[
                "incidents"
            ],
        )

        self.assertNotIn(
            self.incident1,
            response.context[
                "incidents"
            ],
        )


    def test_search_by_incident_number(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "q":
                    self.incident1.incident_number,
            },
        )

        self.assertIn(
            self.incident1,
            response.context[
                "incidents"
            ],
        )

        self.assertEqual(
            len(
                response.context[
                    "incidents"
                ]
            ),
            1,
        )


    def test_filter_by_application(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "application":
                    self.payment_app.pk,
            },
        )

        results = (
            response.context[
                "incidents"
            ]
        )

        self.assertIn(
            self.incident1,
            results,
        )

        self.assertIn(
            self.incident3,
            results,
        )

        self.assertNotIn(
            self.incident2,
            results,
        )


    def test_filter_by_priority(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "priority":
                    Incident.Priority.HIGH,
            },
        )

        results = (
            response.context[
                "incidents"
            ]
        )

        self.assertEqual(
            results,
            [
                self.incident2,
            ],
        )


    def test_filter_by_status(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "status":
                    Incident.Status.NEW,
            },
        )

        results = (
            response.context[
                "incidents"
            ]
        )

        self.assertEqual(
            results,
            [
                self.incident3,
            ],
        )


    def test_filter_by_assigned_user(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "assigned_user":
                    self.operator1.pk,
            },
        )

        results = (
            response.context[
                "incidents"
            ]
        )

        self.assertEqual(
            results,
            [
                self.incident1,
            ],
        )


    def test_filter_by_unassigned(self):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "assigned_user":
                    "unassigned",
            },
        )

        results = (
            response.context[
                "incidents"
            ]
        )

        self.assertEqual(
            results,
            [
                self.incident3,
            ],
        )


    def test_combined_search_and_filters(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "q":
                    "payment",

                "application":
                    self.payment_app.pk,

                "priority":
                    Incident.Priority.CRITICAL,

                "status":
                    Incident.Status.IN_PROGRESS,

                "assigned_user":
                    self.operator1.pk,
            },
        )

        results = (
            response.context[
                "incidents"
            ]
        )

        self.assertEqual(
            results,
            [
                self.incident1,
            ],
        )


    def test_invalid_filter_values_do_not_crash(
        self
    ):

        self.login()

        response = self.client.get(
            reverse("incident_list"),
            {
                "application":
                    "invalid",

                "priority":
                    "INVALID",

                "status":
                    "INVALID",

                "assigned_user":
                    "invalid",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )