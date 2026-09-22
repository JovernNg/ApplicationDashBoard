from django.core.exceptions import ValidationError
from django.utils import timezone

from operations.models import Incident


ALLOWED_TRANSITIONS = {
    Incident.Status.NEW: [
        Incident.Status.ASSIGNED,
    ],

    Incident.Status.ASSIGNED: [
        Incident.Status.IN_PROGRESS,
    ],

    Incident.Status.IN_PROGRESS: [
        Incident.Status.RESOLVED,
    ],

    Incident.Status.RESOLVED: [
        Incident.Status.CLOSED,
    ],

    Incident.Status.CLOSED: [],
}


def get_allowed_transitions(incident):

    return ALLOWED_TRANSITIONS.get(
        incident.status,
        [],
    )


def assign_incident(
    incident,
    assigned_user,
):

    if incident.status in [
        Incident.Status.RESOLVED,
        Incident.Status.CLOSED,
    ]:

        raise ValidationError(
            "Resolved or closed incidents "
            "cannot be reassigned."
        )

    incident.assigned_user = assigned_user

    if incident.status == Incident.Status.NEW:
        incident.status = (
            Incident.Status.ASSIGNED
        )

    incident.save()

    return incident


def transition_incident(
    incident,
    new_status,
    resolution_notes="",
):

    allowed = get_allowed_transitions(
        incident
    )

    if new_status not in allowed:

        raise ValidationError(
            (
                f"Transition from "
                f"{incident.get_status_display()} "
                f"to {new_status} "
                f"is not permitted."
            )
        )

    if (
        new_status
        == Incident.Status.ASSIGNED
        and not incident.assigned_user
    ):

        raise ValidationError(
            "An incident must have an "
            "assigned user before it can "
            "become Assigned."
        )

    if (
        new_status
        == Incident.Status.RESOLVED
    ):

        resolution_notes = (
            resolution_notes.strip()
        )

        if not resolution_notes:

            raise ValidationError(
                "Resolution notes are required "
                "before an incident can be "
                "resolved."
            )

        incident.resolution_notes = (
            resolution_notes
        )

        incident.resolved_at = timezone.now()

    if (
        new_status
        == Incident.Status.CLOSED
    ):

        if not incident.resolved_at:

            raise ValidationError(
                "An incident must be resolved "
                "before it can be closed."
            )

        incident.closed_at = timezone.now()

    incident.status = new_status

    incident.save()

    return incident