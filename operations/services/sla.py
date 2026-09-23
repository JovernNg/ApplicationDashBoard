from datetime import timedelta

from django.utils import timezone

from operations.models import Incident


SLA_TARGETS = {
    Incident.Priority.CRITICAL: timedelta(hours=2),
    Incident.Priority.HIGH: timedelta(hours=4),
    Incident.Priority.MEDIUM: timedelta(hours=8),
    Incident.Priority.LOW: timedelta(hours=24),
}


WITHIN_SLA = "WITHIN_SLA"
AT_RISK = "AT_RISK"
BREACHED = "BREACHED"


SLA_LABELS = {
    WITHIN_SLA: "Within SLA",
    AT_RISK: "At Risk",
    BREACHED: "Breached",
}


def get_sla_target(incident):

    return SLA_TARGETS[
        incident.priority
    ]


def calculate_sla_deadline(incident):

    target = get_sla_target(
        incident
    )

    return (
        incident.reported_at
        + target
    )


def get_sla_reference_time(
    incident,
    current_time=None,
):

    if incident.resolved_at:

        return incident.resolved_at

    if current_time:

        return current_time

    return timezone.now()


def calculate_sla_status(
    incident,
    current_time=None,
):

    target = get_sla_target(
        incident
    )

    deadline = calculate_sla_deadline(
        incident
    )

    reference_time = (
        get_sla_reference_time(
            incident,
            current_time,
        )
    )

    at_risk_time = (
        incident.reported_at
        + (target * 0.75)
    )

    if reference_time >= deadline:

        return BREACHED

    if reference_time >= at_risk_time:

        return AT_RISK

    return WITHIN_SLA


def calculate_sla_progress(
    incident,
    current_time=None,
):

    target = get_sla_target(
        incident
    )

    reference_time = (
        get_sla_reference_time(
            incident,
            current_time,
        )
    )

    elapsed = (
        reference_time
        - incident.reported_at
    )

    total_seconds = (
        target.total_seconds()
    )

    elapsed_seconds = (
        elapsed.total_seconds()
    )

    percentage = (
        elapsed_seconds
        / total_seconds
        * 100
    )

    return max(
        0,
        min(
            percentage,
            100,
        ),
    )