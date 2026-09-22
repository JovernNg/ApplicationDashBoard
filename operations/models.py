from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class Application(models.Model):

    class Status(models.TextChoices):
        HEALTHY = "HEALTHY", "Healthy"
        DEGRADED = "DEGRADED", "Degraded"
        DOWN = "DOWN", "Down"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    owner = models.CharField(
        max_length=150,
    )

    environment = models.CharField(
        max_length=50,
    )

    support_contact = models.EmailField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.HEALTHY,
    )

    availability_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Incident(models.Model):

    class Priority(models.TextChoices):
        CRITICAL = "CRITICAL", "Critical"
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        ASSIGNED = "ASSIGNED", "Assigned"
        IN_PROGRESS = (
            "IN_PROGRESS",
            "In Progress",
        )
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    incident_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.PROTECT,
        related_name="incidents",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reported_incidents",
    )

    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_incidents",
    )

    reported_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    resolution_notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-reported_at",
            "-id",
        ]

    def save(self, *args, **kwargs):

        if self.incident_number:

            return super().save(
                *args,
                **kwargs,
            )

        super().save(
            *args,
            **kwargs,
        )

        self.incident_number = (
            f"INC-"
            f"{self.reported_at:%Y%m%d}-"
            f"{self.pk:04d}"
        )

        super().save(
            update_fields=[
                "incident_number",
            ]
        )

    def __str__(self):

        return (
            f"{self.incident_number} - "
            f"{self.title}"
        )


class AuditLog(models.Model):

    class Action(models.TextChoices):

        APPLICATION_CREATED = (
            "APPLICATION_CREATED",
            "Application Created",
        )

        APPLICATION_UPDATED = (
            "APPLICATION_UPDATED",
            "Application Updated",
        )

        APPLICATION_STATUS_CHANGED = (
            "APPLICATION_STATUS_CHANGED",
            "Application Status Changed",
        )

        INCIDENT_CREATED = (
            "INCIDENT_CREATED",
            "Incident Created",
        )

        INCIDENT_ASSIGNED = (
            "INCIDENT_ASSIGNED",
            "Incident Assigned",
        )

        INCIDENT_STATUS_CHANGED = (
            "INCIDENT_STATUS_CHANGED",
            "Incident Status Changed",
        )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    incident = models.ForeignKey(
        Incident,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=50,
        choices=Action.choices,
    )

    details = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "-created_at",
            "-id",
        ]

    def __str__(self):

        return (
            f"{self.get_action_display()} "
            f"- {self.created_at}"
        )