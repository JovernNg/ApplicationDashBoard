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