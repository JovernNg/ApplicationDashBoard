from django.contrib.auth.models import User
from django.db.models import Q

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
    IncidentAssignmentForm,
    IncidentCreateForm,
    IncidentTransitionForm,
    IncidentUpdateForm,
)

from .models import (
    Application,
    AuditLog,
    Incident,
)

from .services.audit import log_action

from .services.permissions import (
    administrator_required,
    can_manage_incident,
    is_administrator,
)

from django.core.exceptions import (
    PermissionDenied,
    ValidationError,
)

from .services.workflow import (
    assign_incident,
    get_allowed_transitions,
    transition_incident,
)

from .services.sla import (
    BREACHED,
    SLA_LABELS,
    calculate_sla_deadline,
    calculate_sla_progress,
    calculate_sla_status,
    get_sla_target,
)
from django.db import transaction

@login_required
def dashboard(request):

    applications = Application.objects.all()

    incidents = (
        Incident.objects
        .select_related(
            "application",
            "reported_by",
            "assigned_user",
        )
        .all()
    )

    open_statuses = [
        Incident.Status.NEW,
        Incident.Status.ASSIGNED,
        Incident.Status.IN_PROGRESS,
    ]

    open_incidents_qs = (
        incidents.filter(
            status__in=open_statuses
        )
    )

    total_applications = (
        applications.count()
    )

    healthy_applications = (
        applications.filter(
            status=(
                Application.Status.HEALTHY
            )
        ).count()
    )

    problem_applications = (
        applications.filter(
            status__in=[
                Application.Status.DEGRADED,
                Application.Status.DOWN,
            ]
        ).count()
    )

    open_incident_count = (
        open_incidents_qs.count()
    )

    critical_incident_count = (
        open_incidents_qs.filter(
            priority=(
                Incident.Priority.CRITICAL
            )
        ).count()
    )

    open_incidents = list(
        open_incidents_qs
    )

    sla_breach_count = sum(
        1
        for incident in open_incidents
        if calculate_sla_status(
            incident
        ) == BREACHED
    )

    application_status_labels = [
        label
        for value, label
        in Application.Status.choices
    ]

    application_status_data = [
        applications.filter(
            status=value
        ).count()
        for value, label
        in Application.Status.choices
    ]

    incident_priority_labels = [
        label
        for value, label
        in Incident.Priority.choices
    ]

    incident_priority_data = [
        open_incidents_qs.filter(
            priority=value
        ).count()
        for value, label
        in Incident.Priority.choices
    ]

    recent_incidents = list(
        incidents.order_by(
            "-reported_at"
        )[:5]
    )

    for incident in recent_incidents:

        sla_status = (
            calculate_sla_status(
                incident
            )
        )

        incident.sla_status_value = (
            sla_status
        )

        incident.sla_status_label = (
            SLA_LABELS[
                sla_status
            ]
        )

    context = {
        "total_applications":
            total_applications,

        "healthy_applications":
            healthy_applications,

        "problem_applications":
            problem_applications,

        "open_incident_count":
            open_incident_count,

        "critical_incident_count":
            critical_incident_count,

        "sla_breach_count":
            sla_breach_count,

        "application_status_labels":
            application_status_labels,

        "application_status_data":
            application_status_data,

        "incident_priority_labels":
            incident_priority_labels,

        "incident_priority_data":
            incident_priority_data,

        "recent_incidents":
            recent_incidents,

        "is_admin":
            is_administrator(
                request.user
            ),
    }

    return render(
        request,
        "operations/dashboard.html",
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

    query = (
        request.GET
        .get("q", "")
        .strip()
    )

    application_filter = (
        request.GET
        .get("application", "")
        .strip()
    )

    priority_filter = (
        request.GET
        .get("priority", "")
        .strip()
    )

    status_filter = (
        request.GET
        .get("status", "")
        .strip()
    )

    assigned_user_filter = (
        request.GET
        .get("assigned_user", "")
        .strip()
    )


    # Search by incident number,
    # title or description.
    if query:

        incidents = incidents.filter(

            Q(
                incident_number__icontains=query
            )

            |

            Q(
                title__icontains=query
            )

            |

            Q(
                description__icontains=query
            )

        )


    # Application filter.
    if application_filter.isdigit():

        incidents = incidents.filter(
            application_id=int(
                application_filter
            )
        )


    # Priority filter.
    valid_priorities = {
        value
        for value, label
        in Incident.Priority.choices
    }

    if priority_filter in valid_priorities:

        incidents = incidents.filter(
            priority=priority_filter
        )


    # Status filter.
    valid_statuses = {
        value
        for value, label
        in Incident.Status.choices
    }

    if status_filter in valid_statuses:

        incidents = incidents.filter(
            status=status_filter
        )


    # Assigned user filter.
    if assigned_user_filter == "unassigned":

        incidents = incidents.filter(
            assigned_user__isnull=True
        )

    elif assigned_user_filter.isdigit():

        incidents = incidents.filter(
            assigned_user_id=int(
                assigned_user_filter
            )
        )


    incidents = incidents.order_by(
        "-reported_at",
        "-id",
    )


    # Convert to a list before adding
    # calculated SLA information.
    incident_rows = list(
        incidents
    )


    for incident in incident_rows:

        sla_status = (
            calculate_sla_status(
                incident
            )
        )

        incident.sla_status_value = (
            sla_status
        )

        incident.sla_status_label = (
            SLA_LABELS[
                sla_status
            ]
        )

        incident.sla_deadline_value = (
            calculate_sla_deadline(
                incident
            )
        )


    applications = (
        Application.objects
        .order_by("name")
    )


    assigned_users = (
        User.objects
        .filter(
            assigned_incidents__isnull=False
        )
        .distinct()
        .order_by("username")
    )


    context = {

        "incidents":
            incident_rows,

        "applications":
            applications,

        "priority_choices":
            Incident.Priority.choices,

        "status_choices":
            Incident.Status.choices,

        "assigned_users":
            assigned_users,

        "query":
            query,

        "application_filter":
            application_filter,

        "priority_filter":
            priority_filter,

        "status_filter":
            status_filter,

        "assigned_user_filter":
            assigned_user_filter,

        "result_count":
            len(
                incident_rows
            ),
    }


    return render(
        request,
        "operations/incident_list.html",
        context,
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

    is_admin = is_administrator(
        request.user
    )

    can_manage = can_manage_incident(
        request.user,
        incident,
    )

    allowed_transitions = (
        get_allowed_transitions(
            incident
        )
    )

    can_transition = (
        can_manage
        and incident.status
        not in [
            Incident.Status.NEW,
            Incident.Status.CLOSED,
        ]
        and bool(
            allowed_transitions
        )
    )

    can_add_update = (
        can_manage
        and incident.status
        != Incident.Status.CLOSED
    )

    updates = (
        incident.updates
        .select_related(
            "user"
        )
        .all()
    )

    sla_target = get_sla_target(
        incident
    )

    sla_status = (
        calculate_sla_status(
            incident
        )
    )

    sla_deadline = (
        calculate_sla_deadline(
            incident
        )
    )

    sla_progress = (
        calculate_sla_progress(
            incident
        )
    )

    context = {
        "incident":
            incident,

        "is_admin":
            is_admin,

        "can_manage":
            can_manage,

        "can_transition":
            can_transition,

        "can_add_update":
            can_add_update,

        "updates":
            updates,

        "sla_target_hours":
            int(
                sla_target
                .total_seconds()
                // 3600
            ),

        "sla_status":
            sla_status,

        "sla_status_label":
            SLA_LABELS[
                sla_status
            ],

        "sla_deadline":
            sla_deadline,

        "sla_progress":
            round(
                sla_progress,
                1,
            ),
    }

    return render(
        request,
        "operations/incident_detail.html",
        context,
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

@administrator_required
def incident_assign(
    request,
    pk,
):

    incident = get_object_or_404(
        Incident,
        pk=pk,
    )

    if incident.status in [
        Incident.Status.RESOLVED,
        Incident.Status.CLOSED,
    ]:

        messages.error(
            request,
            (
                "Resolved or closed "
                "incidents cannot "
                "be reassigned."
            ),
        )

        return redirect(
            "incident_detail",
            pk=incident.pk,
        )

    if request.method == "POST":

        form = IncidentAssignmentForm(
            request.POST,
            instance=incident,
        )

        if form.is_valid():

            assigned_user = (
                form.cleaned_data[
                    "assigned_user"
                ]
            )

            old_status = (
                incident.status
            )

            with transaction.atomic():

                assign_incident(
                    incident,
                    assigned_user,
                )

                log_action(
                    user=request.user,
                    action=(
                        AuditLog.Action
                        .INCIDENT_ASSIGNED
                    ),
                    application=(
                        incident.application
                    ),
                    incident=incident,
                    details=(
                        f"Incident "
                        f"{incident.incident_number} "
                        f"was assigned to "
                        f"{assigned_user.username}."
                    ),
                )

                if (
                    old_status
                    != incident.status
                ):

                    old_label = dict(
                        Incident.Status.choices
                    )[old_status]

                    new_label = (
                        incident
                        .get_status_display()
                    )

                    log_action(
                        user=request.user,
                        action=(
                            AuditLog.Action
                            .INCIDENT_STATUS_CHANGED
                        ),
                        application=(
                            incident.application
                        ),
                        incident=incident,
                        details=(
                            f"Incident status "
                            f"changed from "
                            f"{old_label} "
                            f"to {new_label}."
                        ),
                    )

            messages.success(
                request,
                (
                    f"Incident "
                    f"{incident.incident_number} "
                    f"was assigned to "
                    f"{assigned_user.username}."
                ),
            )

            return redirect(
                "incident_detail",
                pk=incident.pk,
            )

    else:

        form = IncidentAssignmentForm(
            instance=incident
        )

    return render(
        request,
        "operations/incident_assignment_form.html",
        {
            "form": form,
            "incident": incident,
        },
    )

@login_required
def incident_transition(
    request,
    pk,
):

    incident = get_object_or_404(
        Incident,
        pk=pk,
    )

    if not can_manage_incident(
        request.user,
        incident,
    ):

        raise PermissionDenied

    if (
        incident.status
        == Incident.Status.NEW
    ):

        messages.error(
            request,
            (
                "The incident must be "
                "assigned before its "
                "status can be changed."
            ),
        )

        return redirect(
            "incident_detail",
            pk=incident.pk,
        )

    if (
        incident.status
        == Incident.Status.CLOSED
    ):

        messages.info(
            request,
            "This incident is already closed.",
        )

        return redirect(
            "incident_detail",
            pk=incident.pk,
        )

    if request.method == "POST":

        form = IncidentTransitionForm(
            request.POST,
            incident=incident,
        )

        if form.is_valid():

            new_status = (
                form.cleaned_data[
                    "new_status"
                ]
            )

            resolution_notes = (
                form.cleaned_data.get(
                    "resolution_notes",
                    "",
                )
            )

            old_status = incident.status

            old_label = dict(
                Incident.Status.choices
            )[old_status]

            try:

                with transaction.atomic():

                    transition_incident(
                        incident,
                        new_status,
                        resolution_notes,
                    )

                    new_label = (
                        incident
                        .get_status_display()
                    )

                    log_action(
                        user=request.user,
                        action=(
                            AuditLog.Action
                            .INCIDENT_STATUS_CHANGED
                        ),
                        application=(
                            incident.application
                        ),
                        incident=incident,
                        details=(
                            f"Incident status "
                            f"changed from "
                            f"{old_label} "
                            f"to {new_label}."
                        ),
                    )

            except ValidationError as error:

                form.add_error(
                    None,
                    error.message,
                )

            else:

                messages.success(
                    request,
                    (
                        f"Incident "
                        f"{incident.incident_number} "
                        f"is now "
                        f"{incident.get_status_display()}."
                    ),
                )

                return redirect(
                    "incident_detail",
                    pk=incident.pk,
                )

    else:

        form = IncidentTransitionForm(
            incident=incident
        )

    return render(
        request,
        "operations/incident_transition_form.html",
        {
            "form": form,
            "incident": incident,
        },
    )

@login_required
def incident_update_create(
    request,
    pk,
):

    incident = get_object_or_404(
        Incident,
        pk=pk,
    )

    if not can_manage_incident(
        request.user,
        incident,
    ):

        raise PermissionDenied

    if (
        incident.status
        == Incident.Status.CLOSED
    ):

        messages.error(
            request,
            (
                "Updates cannot be added "
                "to a closed incident."
            ),
        )

        return redirect(
            "incident_detail",
            pk=incident.pk,
        )

    if request.method == "POST":

        form = IncidentUpdateForm(
            request.POST
        )

        if form.is_valid():

            with transaction.atomic():

                update = form.save(
                    commit=False
                )

                update.incident = incident

                update.user = (
                    request.user
                )

                update.save()

                # Refresh the incident's
                # last-updated timestamp.
                incident.save(
                    update_fields=[
                        "updated_at",
                    ]
                )

                log_action(
                    user=request.user,
                    action=(
                        AuditLog.Action
                        .INCIDENT_UPDATE_ADDED
                    ),
                    application=(
                        incident.application
                    ),
                    incident=incident,
                    details=(
                        f"Operational update "
                        f"added to incident "
                        f"{incident.incident_number}."
                    ),
                )

            messages.success(
                request,
                (
                    "Incident update "
                    "was added successfully."
                ),
            )

            return redirect(
                "incident_detail",
                pk=incident.pk,
            )

    else:

        form = IncidentUpdateForm()

    return render(
        request,
        "operations/incident_update_form.html",
        {
            "incident": incident,
            "form": form,
        },
    )

@login_required
def dashboard(request):

    applications = Application.objects.all()

    incidents = (
        Incident.objects
        .select_related(
            "application",
            "reported_by",
            "assigned_user",
        )
        .all()
    )

    open_statuses = [
        Incident.Status.NEW,
        Incident.Status.ASSIGNED,
        Incident.Status.IN_PROGRESS,
    ]

    open_incidents_qs = (
        incidents.filter(
            status__in=open_statuses
        )
    )

    total_applications = (
        applications.count()
    )

    healthy_applications = (
        applications.filter(
            status=Application.Status.HEALTHY
        ).count()
    )

    problem_applications = (
        applications.filter(
            status__in=[
                Application.Status.DEGRADED,
                Application.Status.DOWN,
            ]
        ).count()
    )

    open_incident_count = (
        open_incidents_qs.count()
    )

    critical_incident_count = (
        open_incidents_qs.filter(
            priority=Incident.Priority.CRITICAL
        ).count()
    )

    open_incidents = list(
        open_incidents_qs
    )

    sla_breach_count = sum(
        1
        for incident in open_incidents
        if calculate_sla_status(
            incident
        ) == BREACHED
    )

    application_status_labels = [
        label
        for value, label
        in Application.Status.choices
    ]

    application_status_data = [
        applications.filter(
            status=value
        ).count()
        for value, label
        in Application.Status.choices
    ]

    incident_priority_labels = [
        label
        for value, label
        in Incident.Priority.choices
    ]

    incident_priority_data = [
        open_incidents_qs.filter(
            priority=value
        ).count()
        for value, label
        in Incident.Priority.choices
    ]

    recent_incidents = list(
        incidents.order_by(
            "-reported_at"
        )[:5]
    )

    for incident in recent_incidents:

        sla_status = (
            calculate_sla_status(
                incident
            )
        )

        incident.sla_status_value = (
            sla_status
        )

        incident.sla_status_label = (
            SLA_LABELS[
                sla_status
            ]
        )

    context = {
        "total_applications":
            total_applications,

        "healthy_applications":
            healthy_applications,

        "problem_applications":
            problem_applications,

        "open_incident_count":
            open_incident_count,

        "critical_incident_count":
            critical_incident_count,

        "sla_breach_count":
            sla_breach_count,

        "application_status_labels":
            application_status_labels,

        "application_status_data":
            application_status_data,

        "incident_priority_labels":
            incident_priority_labels,

        "incident_priority_data":
            incident_priority_data,

        "recent_incidents":
            recent_incidents,

        "is_admin":
            is_administrator(
                request.user
            ),
    }

    return render(
        request,
        "operations/dashboard.html",
        context,
    )


@administrator_required
def administrator_test(request):

    return render(
        request,
        "operations/administrator_test.html",
    )