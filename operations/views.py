from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services.permissions import administrator_required


@login_required
def dashboard(request):
    """
    Main operations dashboard.

    The dashboard is deliberately empty for Milestone 1.
    KPI calculations will be added in a later milestone.
    """

    return render(
        request,
        "operations/dashboard.html",
    )


@administrator_required
def administrator_test(request):
    """
    Temporary page for verifying role-based access.

    This can later be replaced by the actual
    application-management page.
    """

    return render(
        request,
        "operations/administrator_test.html",
    )