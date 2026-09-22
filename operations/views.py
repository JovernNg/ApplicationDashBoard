from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import (
    ApplicationForm,
    IncidentCreateForm,
)
from .models import (
    Application,
    AuditLog,
    Incident,
)

from .services.audit import log_action

from .services.permissions import (
    administrator_required,
    is_administrator,
)


@login_required
def dashboard(request):

    return render(
        request,
        "operations/dashboard.html",
        {
            "is_admin": is_administrator(
                request.user
            ),
        },
    )


@administrator_required
def administrator_test(request):

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
def application_detail(
    request,
    pk,
):

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


@administrator_required
def application_create(request):

    if request.method == "POST":

        form = ApplicationForm(
            request.POST
        )

        if form.is_valid():

            application = form.save()

            log_action(
                user=request.user,
                action=(
                    AuditLog.Action
                    .APPLICATION_CREATED
                ),
                application=application,
                details=(
                    f"Application "
                    f"'{application.name}' "
                    f"was registered with "
                    f"status "
                    f"{application.get_status_display()}."
                ),
            )

            messages.success(
                request,
                (
                    f"{application.name} "
                    "was registered successfully."
                ),
            )

            return redirect(
                "application_list"
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

    original_status = application.status

    if request.method == "POST":

        form = ApplicationForm(
            request.POST,
            instance=application,
        )

        if form.is_valid():

            changed_fields = list(
                form.changed_data
            )

            application = form.save()

            if "status" in changed_fields:

                old_status_label = dict(
                    Application.Status.choices
                ).get(
                    original_status,
                    original_status,
                )

                new_status_label = (
                    application
                    .get_status_display()
                )

                log_action(
                    user=request.user,
                    action=(
                        AuditLog.Action
                        .APPLICATION_STATUS_CHANGED
                    ),
                    application=application,
                    details=(
                        f"Application status "
                        f"changed from "
                        f"{old_status_label} "
                        f"to "
                        f"{new_status_label}."
                    ),
                )

            other_fields = [
                field
                for field in changed_fields
                if field != "status"
            ]

            if other_fields:

                field_labels = []

                for field_name in other_fields:

                    field = form.fields.get(
                        field_name
                    )

                    if field:
                        field_labels.append(
                            field.label
                            or field_name
                        )
                    else:
                        field_labels.append(
                            field_name
                        )

                log_action(
                    user=request.user,
                    action=(
                        AuditLog.Action
                        .APPLICATION_UPDATED
                    ),
                    application=application,
                    details=(
                        "Updated fields: "
                        + ", ".join(
                            field_labels
                        )
                        + "."
                    ),
                )

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


@administrator_required
def audit_log_list(request):

    audit_logs = (
        AuditLog.objects
        .select_related(
            "user",
            "application",
        )
        .all()
    )

    return render(
        request,
        "operations/audit_log_list.html",
        {
            "audit_logs": audit_logs,
        },
    )

@login_required
def incident_list(request):

    incidents = (
        Incident.objects
        .select_related(
            "application",
            "reported_by",
            "assigned_user",
        )
        .all()
    )

    return render(
        request,
        "operations/incident_list.html",
        {
            "incidents": incidents,
        },
    )

@login_required
def incident_detail(
    request,
    pk,
):

    incident = get_object_or_404(
        Incident.objects.select_related(
            "application",
            "reported_by",
            "assigned_user",
        ),
        pk=pk,
    )

    return render(
        request,
        "operations/incident_detail.html",
        {
            "incident": incident,
        },
    )

@login_required
def incident_create(request):

    if request.method == "POST":

        form = IncidentCreateForm(
            request.POST
        )

        if form.is_valid():

            incident = form.save(
                commit=False
            )

            incident.reported_by = (
                request.user
            )

            incident.status = (
                Incident.Status.NEW
            )

            incident.save()

            log_action(
                user=request.user,
                action=(
                    AuditLog.Action
                    .INCIDENT_CREATED
                ),
                application=(
                    incident.application
                ),
                incident=incident,
                details=(
                    f"Incident "
                    f"{incident.incident_number} "
                    f"was reported with "
                    f"{incident.get_priority_display()} "
                    f"priority."
                ),
            )

            messages.success(
                request,
                (
                    f"Incident "
                    f"{incident.incident_number} "
                    "was created successfully."
                ),
            )

            return redirect(
                "incident_detail",
                pk=incident.pk,
            )

    else:

        form = IncidentCreateForm()

    return render(
        request,
        "operations/incident_form.html",
        {
            "form": form,
            "page_title":
                "Report Incident",
        },
    )