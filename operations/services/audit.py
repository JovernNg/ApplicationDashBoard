from operations.models import AuditLog


def log_action(
    *,
    user,
    action,
    application=None,
    details="",
):

    return AuditLog.objects.create(
        user=user,
        action=action,
        application=application,
        details=details,
    )