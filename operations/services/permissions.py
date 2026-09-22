from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


ADMINISTRATOR_GROUP = "Administrator"
OPERATIONS_GROUP = "Operations User"


def is_administrator(user):
    """
    Returns True if the user is either:
    - a Django superuser, or
    - a member of the Administrator group.
    """

    if not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or user.groups.filter(
            name=ADMINISTRATOR_GROUP
        ).exists()
    )


def is_operations_user(user):
    """
    Administrator is also treated as an operations user
    because the Administrator inherits the normal
    operational capabilities.
    """

    if not user.is_authenticated:
        return False

    return (
        is_administrator(user)
        or user.groups.filter(
            name=OPERATIONS_GROUP
        ).exists()
    )


def administrator_required(view_func):
    """
    Logged-out users are redirected to login.

    Authenticated users without Administrator permission
    receive HTTP 403.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path()
            )

        if not is_administrator(request.user):
            raise PermissionDenied

        return view_func(
            request,
            *args,
            **kwargs,
        )

    return wrapper

def can_manage_incident(
    user,
    incident,
):

    if not user.is_authenticated:
        return False

    if is_administrator(user):
        return True

    if is_operations_user(user):

        return (
            incident.assigned_user_id
            == user.id
        )

    return False