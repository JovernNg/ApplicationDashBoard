from django.contrib import admin

from .models import (
    Application,
    AuditLog,
    Incident,
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "environment",
        "owner",
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


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = [
        "created_at",
        "user",
        "action",
        "application",
    ]

    list_filter = [
        "action",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "application__name",
        "details",
    ]

    readonly_fields = [
        "user",
        "application",
        "action",
        "details",
        "created_at",
    ]

    def has_add_permission(
        self,
        request,
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ):
        return False

    @admin.register(Incident)
    class IncidentAdmin(admin.ModelAdmin):

        list_display = [
            "incident_number",
            "application",
            "title",
            "priority",
            "status",
            "reported_by",
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
            "application__name",
        ]

        readonly_fields = [
            "incident_number",
            "reported_at",
            "updated_at",
        ]