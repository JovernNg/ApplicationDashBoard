from django.contrib import admin

from .models import (
    Application,
    AuditLog,
    Incident,
    IncidentUpdate,
)


class ReadOnlyAdminMixin:

    def has_add_permission(
        self,
        request,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False


@admin.register(Application)
class ApplicationAdmin(
    ReadOnlyAdminMixin,
    admin.ModelAdmin,
):

    list_display = [
        "name",
        "owner",
        "environment",
        "status",
        "availability_percentage",
        "updated_at",
    ]

    list_filter = [
        "status",
        "environment",
    ]

    search_fields = [
        "name",
        "owner",
        "support_contact",
    ]


@admin.register(Incident)
class IncidentAdmin(
    ReadOnlyAdminMixin,
    admin.ModelAdmin,
):

    list_display = [
        "incident_number",
        "application",
        "title",
        "priority",
        "status",
        "assigned_user",
        "reported_at",
    ]

    list_filter = [
        "priority",
        "status",
        "application",
    ]

    search_fields = [
        "incident_number",
        "title",
        "description",
    ]


@admin.register(IncidentUpdate)
class IncidentUpdateAdmin(
    ReadOnlyAdminMixin,
    admin.ModelAdmin,
):

    list_display = [
        "created_at",
        "incident",
        "user",
    ]

    search_fields = [
        "incident__incident_number",
        "user__username",
        "update_text",
    ]


@admin.register(AuditLog)
class AuditLogAdmin(
    ReadOnlyAdminMixin,
    admin.ModelAdmin,
):

    list_display = [
        "created_at",
        "user",
        "action",
        "application",
        "incident",
    ]

    list_filter = [
        "action",
        "created_at",
    ]

    search_fields = [
        "details",
        "application__name",
        "incident__incident_number",
        "user__username",
    ]