from django.contrib.auth.models import (
    Group,
    User,
)
from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse

from operations.models import (
    Application,
    Incident,
    IncidentUpdate,
)


class SecurityTests(TestCase):

    def setUp(self):

        self.admin_group = Group.objects.create(
            name="Administrator"
        )

        self.operations_group = Group.objects.create(
            name="Operations User"
        )

        self.admin = User.objects.create_user(
            username="security_admin",
            password="TestPassword123!",
        )

        self.admin.groups.add(
            self.admin_group
        )

        self.operator1 = User.objects.create_user(
            username="security_operator1",
            password="TestPassword123!",
        )

        self.operator1.groups.add(
            self.operations_group
        )

        self.operator2 = User.objects.create_user(
            username="security_operator2",
            password="TestPassword123!",
        )

        self.operator2.groups.add(
            self.operations_group
        )

        self.superuser = User.objects.create_superuser(
            username="security_superuser",
            email="security@example.com",
            password="TestPassword123!",
        )

        self.application = Application.objects.create(
            name="Security Test Application",
            description="Application used for security testing.",
            owner="Operations",
            environment="Production",
            support_contact="support@example.com",
            status=Application.Status.HEALTHY,
            availability_percentage=100,
        )

        self.incident = Incident.objects.create(
            application=self.application,
            title="Security Test Incident",
            description="Incident used for security testing.",
            priority=Incident.Priority.HIGH,
            status=Incident.Status.ASSIGNED,
            reported_by=self.admin,
            assigned_user=self.operator1,
        )

    def login_operator1(self):

        return self.client.login(
            username="security_operator1",
            password="TestPassword123!",
        )

    def login_operator2(self):

        return self.client.login(
            username="security_operator2",
            password="TestPassword123!",
        )

    def test_anonymous_user_cannot_access_protected_pages(
        self
    ):

        urls = [
            reverse("dashboard"),
            reverse("application_list"),
            reverse("incident_list"),
            reverse(
                "incident_detail",
                args=[self.incident.pk],
            ),
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

    def test_operator_cannot_access_application_create_direct_url(
        self
    ):

        self.login_operator1()

        response = self.client.get(
            reverse(
                "application_create"
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_operator_cannot_access_application_edit_direct_url(
        self
    ):

        self.login_operator1()

        response = self.client.get(
            reverse(
                "application_edit",
                args=[
                    self.application.pk
                ],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_operator_cannot_access_audit_log_direct_url(
        self
    ):

        self.login_operator1()

        response = self.client.get(
            reverse(
                "audit_log_list"
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_unassigned_operator_cannot_transition_incident_directly(
        self
    ):

        self.login_operator2()

        response = self.client.get(
            reverse(
                "incident_transition",
                args=[
                    self.incident.pk
                ],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_unassigned_operator_cannot_add_update_directly(
        self
    ):

        self.login_operator2()

        response = self.client.get(
            reverse(
                "incident_update_create",
                args=[
                    self.incident.pk
                ],
            )
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_csrf_blocks_incident_update_without_token(
        self
    ):

        csrf_client = Client(
            enforce_csrf_checks=True
        )

        logged_in = csrf_client.login(
            username="security_operator1",
            password="TestPassword123!",
        )

        self.assertTrue(
            logged_in
        )

        response = csrf_client.post(
            reverse(
                "incident_update_create",
                args=[
                    self.incident.pk
                ],
            ),
            {
                "update_text":
                    "Attempt without CSRF token.",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            IncidentUpdate.objects.filter(
                update_text=(
                    "Attempt without CSRF token."
                )
            ).exists()
        )

    def test_xss_payload_is_escaped_in_timeline(
        self
    ):

        payload = (
            "<script>alert('xss')</script>"
        )

        IncidentUpdate.objects.create(
            incident=self.incident,
            user=self.operator1,
            update_text=payload,
        )

        self.login_operator1()

        response = self.client.get(
            reverse(
                "incident_detail",
                args=[
                    self.incident.pk
                ],
            )
        )

        content = response.content.decode(
            "utf-8"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertNotIn(
            payload,
            content,
        )

        self.assertIn(
            "&lt;script&gt;",
            content,
        )

    def test_sql_injection_style_search_is_treated_as_text(
        self
    ):

        Incident.objects.create(
            application=self.application,
            title="Second Security Incident",
            description="Another incident.",
            priority=Incident.Priority.LOW,
            status=Incident.Status.NEW,
            reported_by=self.admin,
        )

        self.login_operator1()

        response = self.client.get(
            reverse(
                "incident_list"
            ),
            {
                "q":
                    "' OR 1=1 --",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.context[
                "result_count"
            ],
            0,
        )

    def test_logout_invalidates_authenticated_session(
        self
    ):

        self.login_operator1()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.client.post(
            reverse("logout")
        )

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            reverse("login"),
            response.url,
        )

    def test_incident_create_ignores_protected_field_tampering(
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
                    "Parameter Tampering Test",

                "description":
                    "Attempt to manipulate protected fields.",

                "priority":
                    Incident.Priority.MEDIUM,

                "status":
                    Incident.Status.CLOSED,

                "assigned_user":
                    self.operator2.pk,

                "reported_by":
                    self.operator2.pk,
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        incident = Incident.objects.get(
            title="Parameter Tampering Test"
        )

        self.assertEqual(
            incident.status,
            Incident.Status.NEW,
        )

        self.assertIsNone(
            incident.assigned_user
        )

        self.assertEqual(
            incident.reported_by,
            self.operator1,
        )

    def test_closed_incident_rejects_direct_update(
        self
    ):

        self.incident.status = (
            Incident.Status.CLOSED
        )

        self.incident.save()

        self.login_operator1()

        response = self.client.post(
            reverse(
                "incident_update_create",
                args=[
                    self.incident.pk
                ],
            ),
            {
                "update_text":
                    "Attempt to modify closed incident.",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            IncidentUpdate.objects.filter(
                incident=self.incident,
                update_text=(
                    "Attempt to modify closed incident."
                ),
            ).exists()
        )

    def test_django_admin_cannot_bypass_incident_workflow(
        self
    ):

        admin_client = Client()

        logged_in = admin_client.login(
            username="security_superuser",
            password="TestPassword123!",
        )

        self.assertTrue(
            logged_in
        )

        original_status = (
            self.incident.status
        )

        response = admin_client.post(
            reverse(
                "admin:operations_incident_change",
                args=[
                    self.incident.pk
                ],
            ),
            {
                "status":
                    Incident.Status.CLOSED,
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.incident.refresh_from_db()

        self.assertEqual(
            self.incident.status,
            original_status,
        )

    def test_django_admin_cannot_bypass_application_controls(
        self
    ):

        admin_client = Client()

        logged_in = admin_client.login(
            username="security_superuser",
            password="TestPassword123!",
        )

        self.assertTrue(
            logged_in
        )

        original_name = (
            self.application.name
        )

        response = admin_client.post(
            reverse(
                "admin:operations_application_change",
                args=[
                    self.application.pk
                ],
            ),
            {
                "name":
                    "Tampered Application Name",
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.application.refresh_from_db()

        self.assertEqual(
            self.application.name,
            original_name,
        )