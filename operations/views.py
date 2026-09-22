from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import ApplicationForm
from .models import Application

from .services.permissions import (
    administrator_required,
    is_administrator,
)

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


@login_required
def application_list(request):

    applications = Application.objects.all()

    context = {
        "applications": applications,
        "is_admin": is_administrator(
            request.user
        ),
    }

    return render(
        request,
        "operations/application_list.html",
        context,
    )


@login_required
def application_list(request):

    applications = Application.objects.all()

    context = {
        "applications": applications,
        "is_admin": is_administrator(
            request.user
        ),
    }

    return render(
        request,
        "operations/application_list.html",
        context,
    )


@administrator_required
def application_create(request):

    if request.method == "POST":

        form = ApplicationForm(
            request.POST
        )

        if form.is_valid():

            application = form.save()

            messages.success(
                request,
                (
                    f"{application.name} "
                    "was registered successfully."
                ),
            )

            return redirect(
                "application_detail",
                pk=application.pk,
            )

    else:

        form = ApplicationForm()

    return render(
        request,
        "operations/application_form.html",
        {
            "form": form,
            "page_title":
                "Register Application",
        },
    )


@administrator_required
def application_edit(
    request,
    pk,
):

    application = get_object_or_404(
        Application,
        pk=pk,
    )

    if request.method == "POST":

        form = ApplicationForm(
            request.POST,
            instance=application,
        )

        if form.is_valid():

            application = form.save()

            messages.success(
                request,
                (
                    f"{application.name} "
                    "was updated successfully."
                ),
            )

            return redirect(
                "application_detail",
                pk=application.pk,
            )

    else:

        form = ApplicationForm(
            instance=application
        )

    return render(
        request,
        "operations/application_form.html",
        {
            "form": form,
            "page_title":
                "Edit Application",
            "application":
                application,
        },
    )

@login_required
def application_detail(request, pk):

    application = get_object_or_404(
        Application,
        pk=pk,
    )

    context = {
        "application": application,
        "is_admin": is_administrator(
            request.user
        ),
    }

    return render(
        request,
        "operations/application_detail.html",
        context,
    )