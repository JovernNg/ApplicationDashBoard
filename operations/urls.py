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
]