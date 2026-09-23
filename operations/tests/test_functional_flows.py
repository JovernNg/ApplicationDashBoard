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


class FunctionalWorkflowTests(TestCase):

    def setUp(self):

        self.admin_group = Group.objects.create(
            name="Administrator"
        )

        self.operations_group = Group.objects.create(
            name="Operations User"
        )

        self.admin = User.objects.create_user(
            username="functional_admin",
            password="TestPassword123!",
        )

        self.admin.groups.add(
            self.admin_group
        )

        self.operator1 = User.objects.create_user(
            username="functional_operator1",
            password="TestPassword123!",
        )

        self.operator1.groups.add(
            self.operations_group
        )

        self.operator2 = User.objects.create_user(
            username="functional_operator2",
            password="TestPassword123!",
        )

        self.operator2.groups.add(
            self.operations_group
        )

        self.application = Application.objects.create(
            name="Functional Test Application",
            description="Application used for functional testing.",
            owner="Operations",
            environment="Production",
            support_contact="support@example.com",
            status=Application.Status.HEALTHY,
            availability_percentage=100,
        )

    def login_admin(self):

        return self.client.login(
            username="functional_admin",
            password="TestPassword123!",
        )

    def login_operator1(self):

        return self.client.login(
            username="functional_operator1",
            password="TestPassword123!",
        )

    def login_operator2(self):

        return self.client.login(
            username="functional_operator2",
            password="TestPassword123!",
        )

    def create_incident(
        self,
        status=Incident.Status.NEW,
        assigned_user=None,
    ):

        return Incident.objects.create(
            application=self.application,
            title="Functional Test Incident",
            description="Functional workflow test incident.",
            priority=Incident.Priority.CRITICAL,
            status=status,
            reported_by=self.admin,
            assigned_user=assigned_user,
        )

    def test_authenticated_pages_require_login(self):

        urls = [
            reverse("dashboard"),
            reverse("application_list"),
            reverse("incident_list"),
        ]

        for url in urls:

            response = self.client.get(
                url
            )

            self.assertEqual(
                response.status_code,
                302,
            )

            self.assertIn(
                reverse("login"),
                response.url,
            )

    def test_administrator_can_create_application(self):

        self.login_admin()

        response = self.client.post(
            reverse(
                "application_create"
            ),
            {
                "name":
                    "New Functional Application",

                "description":
                    "Created during functional testing.",

                "owner":
                    "Operations",

                "environment":
                    "Production",

                "support_contact":
                    "newapp@example.com",

                "status":
                    Application.Status.HEALTHY,

                "availability_percentage":
                    "99.50",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        application = Application.objects.get(
            name="New Functional Application"
        )

        self.assertEqual(
            application.owner,
            "Operations",
        )

        self.assertTrue(
            AuditLog.objects.filter(
                application=application,
                action=(
                    AuditLog.Action
                    .APPLICATION_CREATED
                ),
            ).exists()
        )

    def test_operations_user_cannot_manage_applications(
        self
    ):

        self.login_operator1()

        create_response = self.client.get(
            reverse(
                "application_create"
            )
        )

        edit_response = self.client.get(
            reverse(
                "application_edit",
                args=[
                    self.application.pk
                ],
            )
        )

        self.assertEqual(
            create_response.status_code,
            403,
        )

        self.assertEqual(
            edit_response.status_code,
            403,
        )

    def test_operations_user_can_report_incident(
        self
    ):

        self.login_operator1()

        response = self.client.post(
            reverse(
                "incident_create"
            ),
            {
                "application":
                    self.application.pk,

                "title":
                    "Reported Functional Incident",

                "description":
                    "Reported by operations user.",

                "priority":
                    Incident.Priority.HIGH,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        incident = Incident.objects.get(
            title="Reported Functional Incident"
        )

        self.assertEqual(
            incident.status,
            Incident.Status.NEW,
        )

        self.assertEqual(
            incident.reported_by,
            self.operator1,
        )

        self.assertTrue(
            incident.incident_number
        )

        self.assertTrue(
            AuditLog.objects.filter(
                incident=incident,
                action=(
                    AuditLog.Action
                    .INCIDENT_CREATED
                ),
            ).exists()
        )

    def test_administrator_can_assign_incident(
        self
    ):

        incident = self.create_incident()

        self.login_admin()

        response = self.client.post(
            reverse(
                "incident_assign",
                args=[
                    incident.pk
                ],
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

        incident.refresh_from_db()

        self.assertEqual(
            incident.assigned_user,
            self.operator1,
        )

        self.assertEqual(
            incident.status,
            Incident.Status.ASSIGNED,
        )

        self.assertTrue(
            AuditLog.objects.filter(
                incident=incident,
                action=(
                    AuditLog.Action
                    .INCIDENT_ASSIGNED
                ),
            ).exists()
        )

    def test_complete_incident_workflow(
        self
    ):

        incident = self.create_incident(
            status=Incident.Status.ASSIGNED,
            assigned_user=self.operator1,
        )

        self.login_operator1()

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[
                    incident.pk
                ],
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

        incident.refresh_from_db()

        self.assertEqual(
            incident.status,
            Incident.Status.IN_PROGRESS,
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[
                    incident.pk
                ],
            ),
            {
                "new_status":
                    Incident.Status.RESOLVED,

                "resolution_notes":
                    (
                        "Root cause identified "
                        "and service restored."
                    ),
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        incident.refresh_from_db()

        self.assertEqual(
            incident.status,
            Incident.Status.RESOLVED,
        )

        self.assertIsNotNone(
            incident.resolved_at
        )

        self.assertEqual(
            incident.resolution_notes,
            (
                "Root cause identified "
                "and service restored."
            ),
        )

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[
                    incident.pk
                ],
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

        incident.refresh_from_db()

        self.assertEqual(
            incident.status,
            Incident.Status.CLOSED,
        )

        self.assertIsNotNone(
            incident.closed_at
        )

    def test_resolution_requires_notes(self):

        incident = self.create_incident(
            status=Incident.Status.IN_PROGRESS,
            assigned_user=self.operator1,
        )

        self.login_operator1()

        response = self.client.post(
            reverse(
                "incident_transition",
                args=[
                    incident.pk
                ],
            ),
            {
                "new_status":
                    Incident.Status.RESOLVED,

                "resolution_notes":
                    "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        incident.refresh_from_db()

        self.assertEqual(
            incident.status,
            Incident.Status.IN_PROGRESS,
        )

        self.assertIsNone(
            incident.resolved_at
        )

    def test_unassigned_operator_cannot_manage_incident(
        self
    ):

        incident = self.create_incident(
            status=Incident.Status.ASSIGNED,
            assigned_user=self.operator1,
        )

        self.login_operator2()

        transition_response = (
            self.client.get(
                reverse(
                    "incident_transition",
                    args=[
                        incident.pk
                    ],
                )
            )
        )

        update_response = (
            self.client.get(
                reverse(
                    "incident_update_create",
                    args=[
                        incident.pk
                    ],
                )
            )
        )

        self.assertEqual(
            transition_response.status_code,
            403,
        )

        self.assertEqual(
            update_response.status_code,
            403,
        )

    def test_incident_update_is_recorded_and_audited(
        self
    ):

        incident = self.create_incident(
            status=Incident.Status.IN_PROGRESS,
            assigned_user=self.operator1,
        )

        self.login_operator1()

        response = self.client.post(
            reverse(
                "incident_update_create",
                args=[
                    incident.pk
                ],
            ),
            {
                "update_text":
                    (
                        "Application logs checked. "
                        "Recovery work is in progress."
                    ),
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        update = IncidentUpdate.objects.get(
            incident=incident
        )

        self.assertEqual(
            update.user,
            self.operator1,
        )

        self.assertIn(
            "Recovery work",
            update.update_text,
        )

        self.assertTrue(
            AuditLog.objects.filter(
                incident=incident,
                action=(
                    AuditLog.Action
                    .INCIDENT_UPDATE_ADDED
                ),
            ).exists()
        )

    def test_search_finds_incident(
        self
    ):

        incident = self.create_incident()

        incident.title = (
            "Database Connection Failure"
        )

        incident.save()

        self.login_operator1()

        response = self.client.get(
            reverse(
                "incident_list"
            ),
            {
                "q":
                    "database connection",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            incident.incident_number,
        )

        self.assertContains(
            response,
            "Database Connection Failure",
        )

    def test_dashboard_displays_operational_data(
        self
    ):

        self.create_incident()

        self.login_operator1()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.context[
                "total_applications"
            ],
            1,
        )

        self.assertEqual(
            response.context[
                "open_incident_count"
            ],
            1,
        )

        self.assertContains(
            response,
            "Functional Test Incident",
        )