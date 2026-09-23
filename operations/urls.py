from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "administrator-test/",
        views.administrator_test,
        name="administrator_test",
    ),

    path(
        "applications/",
        views.application_list,
        name="application_list",
    ),

    path(
        "applications/new/",
        views.application_create,
        name="application_create",
    ),

    path(
        "applications/<int:pk>/",
        views.application_detail,
        name="application_detail",
    ),

    path(
        "applications/<int:pk>/edit/",
        views.application_edit,
        name="application_edit",
    ),

    path(
        "audit/",
        views.audit_log_list,
        name="audit_log_list",
    ),

    path(
    "incidents/",
    views.incident_list,
    name="incident_list",
),

path(
    "incidents/new/",
    views.incident_create,
    name="incident_create",
),

path(
    "incidents/<int:pk>/",
    views.incident_detail,
    name="incident_detail",
),

path(
    "incidents/<int:pk>/assign/",
    views.incident_assign,
    name="incident_assign",
),

path(
    "incidents/<int:pk>/transition/",
    views.incident_transition,
    name="incident_transition",
),

path(
    "incidents/<int:pk>/updates/new/",
    views.incident_update_create,
    name="incident_update_create",
),
]