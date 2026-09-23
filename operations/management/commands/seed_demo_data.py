from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import (
    Group,
    User,
)
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from operations.models import (
    Application,
    AuditLog,
    Incident,
    IncidentUpdate,
)


ADMIN_GROUP = "Administrator"
OPERATIONS_GROUP = "Operations User"

DEMO_USERS = [
    "demo_admin",
    "demo_operator1",
    "demo_operator2",
]

DEMO_APPLICATIONS = [
    "Demo Payment Portal",
    "Demo Customer Portal",
    "Demo Reporting Service",
    "Demo HR Self Service",
]


class Command(BaseCommand):

    help = (
        "Create a repeatable demonstration dataset "
        "for the final project demonstration."
    )

    def handle(
        self,
        *args,
        **options,
    ):

        self.stdout.write(
            "Preparing demonstration data..."
        )

        self.remove_existing_demo_data()

        administrator_group, _ = (
            Group.objects.get_or_create(
                name=ADMIN_GROUP
            )
        )

        operations_group, _ = (
            Group.objects.get_or_create(
                name=OPERATIONS_GROUP
            )
        )

        demo_admin = User.objects.create_user(
            username="demo_admin",
            password="DemoPass123!",
        )

        demo_admin.groups.add(
            administrator_group
        )

        demo_operator1 = User.objects.create_user(
            username="demo_operator1",
            password="DemoPass123!",
        )

        demo_operator1.groups.add(
            operations_group
        )

        demo_operator2 = User.objects.create_user(
            username="demo_operator2",
            password="DemoPass123!",
        )

        demo_operator2.groups.add(
            operations_group
        )

        payment_app = Application.objects.create(
            name="Demo Payment Portal",
            description=(
                "Customer-facing payment "
                "processing application."
            ),
            owner="Digital Payments",
            environment="Production",
            support_contact=(
                "payments@example.com"
            ),
            status=(
                Application.Status.HEALTHY
            ),
            availability_percentage=(
                Decimal("99.98")
            ),
        )

        customer_app = Application.objects.create(
            name="Demo Customer Portal",
            description=(
                "Customer account and "
                "self-service portal."
            ),
            owner="Customer Services",
            environment="Production",
            support_contact=(
                "customer@example.com"
            ),
            status=(
                Application.Status.DEGRADED
            ),
            availability_percentage=(
                Decimal("98.75")
            ),
        )

        reporting_app = Application.objects.create(
            name="Demo Reporting Service",
            description=(
                "Operational and management "
                "reporting service."
            ),
            owner="Data Services",
            environment="Production",
            support_contact=(
                "reporting@example.com"
            ),
            status=(
                Application.Status.DOWN
            ),
            availability_percentage=(
                Decimal("95.20")
            ),
        )

        hr_app = Application.objects.create(
            name="Demo HR Self Service",
            description=(
                "Employee self-service "
                "application."
            ),
            owner="Human Resources",
            environment="Production",
            support_contact=(
                "hr@example.com"
            ),
            status=(
                Application.Status.MAINTENANCE
            ),
            availability_percentage=(
                Decimal("99.90")
            ),
        )

        now = timezone.now().replace(
            microsecond=0
        )

        critical_incident = (
            Incident.objects.create(
                application=reporting_app,
                title=(
                    "Reporting Service "
                    "Unavailable"
                ),
                description=(
                    "Users cannot access "
                    "operational reports."
                ),
                priority=(
                    Incident.Priority.CRITICAL
                ),
                status=(
                    Incident.Status.IN_PROGRESS
                ),
                reported_by=demo_admin,
                assigned_user=demo_operator1,
            )
        )

        self.set_reported_time(
            critical_incident,
            now - timedelta(hours=3),
        )

        high_incident = (
            Incident.objects.create(
                application=customer_app,
                title=(
                    "Customer Login "
                    "Performance Degradation"
                ),
                description=(
                    "Login requests are "
                    "responding more slowly "
                    "than normal."
                ),
                priority=(
                    Incident.Priority.HIGH
                ),
                status=(
                    Incident.Status.ASSIGNED
                ),
                reported_by=demo_admin,
                assigned_user=demo_operator2,
            )
        )

        self.set_reported_time(
            high_incident,
            now - timedelta(
                hours=3,
                minutes=15,
            ),
        )

        medium_incident = (
            Incident.objects.create(
                application=payment_app,
                title=(
                    "Delayed Payment "
                    "Confirmation"
                ),
                description=(
                    "Some confirmation "
                    "messages are delayed."
                ),
                priority=(
                    Incident.Priority.MEDIUM
                ),
                status=(
                    Incident.Status.IN_PROGRESS
                ),
                reported_by=demo_operator1,
                assigned_user=demo_operator1,
            )
        )

        self.set_reported_time(
            medium_incident,
            now - timedelta(hours=2),
        )

        new_incident = (
            Incident.objects.create(
                application=payment_app,
                title=(
                    "Intermittent Receipt "
                    "Generation Failure"
                ),
                description=(
                    "A small number of "
                    "receipts are not generated."
                ),
                priority=(
                    Incident.Priority.LOW
                ),
                status=(
                    Incident.Status.NEW
                ),
                reported_by=demo_operator2,
            )
        )

        self.set_reported_time(
            new_incident,
            now - timedelta(minutes=45),
        )

        resolved_incident = (
            Incident.objects.create(
                application=customer_app,
                title=(
                    "Profile Update Error"
                ),
                description=(
                    "Customers were unable "
                    "to save profile changes."
                ),
                priority=(
                    Incident.Priority.HIGH
                ),
                status=(
                    Incident.Status.RESOLVED
                ),
                reported_by=demo_admin,
                assigned_user=demo_operator1,
                resolved_at=(
                    now - timedelta(hours=2)
                ),
                resolution_notes=(
                    "Configuration issue "
                    "corrected and profile "
                    "updates validated."
                ),
            )
        )

        self.set_reported_time(
            resolved_incident,
            now - timedelta(hours=5),
        )

        closed_incident = (
            Incident.objects.create(
                application=payment_app,
                title=(
                    "Payment Notification "
                    "Queue Delay"
                ),
                description=(
                    "Payment notifications "
                    "were temporarily delayed."
                ),
                priority=(
                    Incident.Priority.LOW
                ),
                status=(
                    Incident.Status.CLOSED
                ),
                reported_by=demo_admin,
                assigned_user=demo_operator2,
                resolved_at=(
                    now - timedelta(
                        days=1,
                        hours=19,
                    )
                ),
                closed_at=(
                    now - timedelta(
                        days=1,
                        hours=18,
                    )
                ),
                resolution_notes=(
                    "Notification queue "
                    "restarted and backlog "
                    "processed successfully."
                ),
            )
        )

        self.set_reported_time(
            closed_incident,
            now - timedelta(days=2),
        )

        self.create_update(
            incident=critical_incident,
            user=demo_operator1,
            text=(
                "Initial investigation "
                "confirmed reporting service "
                "connection failures."
            ),
            created_at=(
                now - timedelta(
                    hours=2,
                    minutes=30,
                )
            ),
        )

        self.create_update(
            incident=critical_incident,
            user=demo_operator1,
            text=(
                "Database connectivity has "
                "been restored. Service "
                "validation is in progress."
            ),
            created_at=(
                now - timedelta(hours=1)
            ),
        )

        self.create_update(
            incident=medium_incident,
            user=demo_operator1,
            text=(
                "Message queue checked. "
                "Confirmation backlog is "
                "being processed."
            ),
            created_at=(
                now - timedelta(minutes=45)
            ),
        )

        self.create_update(
            incident=resolved_incident,
            user=demo_operator1,
            text=(
                "Configuration corrected and "
                "successful profile update "
                "confirmed."
            ),
            created_at=(
                now - timedelta(
                    hours=2,
                    minutes=5,
                )
            ),
        )

        applications = [
            payment_app,
            customer_app,
            reporting_app,
            hr_app,
        ]

        for application in applications:

            self.create_audit(
                user=demo_admin,
                application=application,
                incident=None,
                action=(
                    AuditLog.Action
                    .APPLICATION_CREATED
                ),
                details=(
                    f"Application "
                    f"{application.name} "
                    f"created for "
                    f"demonstration data."
                ),
                created_at=(
                    now - timedelta(days=3)
                ),
            )

        incidents = [
            critical_incident,
            high_incident,
            medium_incident,
            new_incident,
            resolved_incident,
            closed_incident,
        ]

        for incident in incidents:

            self.create_audit(
                user=(
                    incident.reported_by
                ),
                application=(
                    incident.application
                ),
                incident=incident,
                action=(
                    AuditLog.Action
                    .INCIDENT_CREATED
                ),
                details=(
                    f"Incident "
                    f"{incident.incident_number} "
                    f"created."
                ),
                created_at=(
                    incident.reported_at
                ),
            )

            if incident.assigned_user:

                self.create_audit(
                    user=demo_admin,
                    application=(
                        incident.application
                    ),
                    incident=incident,
                    action=(
                        AuditLog.Action
                        .INCIDENT_ASSIGNED
                    ),
                    details=(
                        f"Incident assigned "
                        f"to "
                        f"{incident.assigned_user.username}."
                    ),
                    created_at=(
                        incident.reported_at
                        + timedelta(minutes=10)
                    ),
                )

        self.stdout.write(
            ""
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created successfully."
            )
        )

        self.stdout.write(
            ""
        )

        self.stdout.write(
            "Demo accounts:"
        )

        self.stdout.write(
            "demo_admin / DemoPass123!"
        )

        self.stdout.write(
            "demo_operator1 / DemoPass123!"
        )

        self.stdout.write(
            "demo_operator2 / DemoPass123!"
        )

        self.stdout.write(
            ""
        )

        self.stdout.write(
            (
                "Applications created: "
                f"{len(applications)}"
            )
        )

        self.stdout.write(
            (
                "Incidents created: "
                f"{len(incidents)}"
            )
        )

    def remove_existing_demo_data(
        self
    ):

        demo_apps = (
            Application.objects.filter(
                name__in=DEMO_APPLICATIONS
            )
        )

        demo_incidents = (
            Incident.objects.filter(
                application__in=demo_apps
            )
        )

        AuditLog.objects.filter(
            Q(
                application__in=demo_apps
            )
            |
            Q(
                incident__in=demo_incidents
            )
        ).delete()

        demo_incidents.delete()

        demo_apps.delete()

        User.objects.filter(
            username__in=DEMO_USERS
        ).delete()

    def set_reported_time(
        self,
        incident,
        reported_at,
    ):

        incident_number = (
            f"INC-"
            f"{reported_at:%Y%m%d}-"
            f"{incident.pk:04d}"
        )

        Incident.objects.filter(
            pk=incident.pk
        ).update(
            reported_at=reported_at,
            incident_number=incident_number,
        )

        incident.refresh_from_db()

    def create_update(
        self,
        incident,
        user,
        text,
        created_at,
    ):

        update = (
            IncidentUpdate.objects.create(
                incident=incident,
                user=user,
                update_text=text,
            )
        )

        IncidentUpdate.objects.filter(
            pk=update.pk
        ).update(
            created_at=created_at
        )

        self.create_audit(
            user=user,
            application=incident.application,
            incident=incident,
            action=(
                AuditLog.Action
                .INCIDENT_UPDATE_ADDED
            ),
            details=(
                f"Operational update added "
                f"to incident "
                f"{incident.incident_number}."
            ),
            created_at=created_at,
        )

    def create_audit(
        self,
        user,
        application,
        incident,
        action,
        details,
        created_at,
    ):

        audit = AuditLog.objects.create(
            user=user,
            application=application,
            incident=incident,
            action=action,
            details=details,
        )

        AuditLog.objects.filter(
            pk=audit.pk
        ).update(
            created_at=created_at
        )