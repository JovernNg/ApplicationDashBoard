from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "administrator-test/",
        views.administrator_test,
        name="administrator_test",
    ),
]