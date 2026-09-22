from django.contrib import admin

from .models import Application


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