import statistics
import time
from getpass import getpass

from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.test import Client
from django.urls import reverse

from operations.models import (
    Application,
    Incident,
)


class Command(BaseCommand):

    help = (
        "Measure response times for "
        "main application pages."
    )

    def add_arguments(
        self,
        parser,
    ):

        parser.add_argument(
            "--username",
            required=True,
            help=(
                "Username used to access "
                "authenticated pages."
            ),
        )

        parser.add_argument(
            "--runs",
            type=int,
            default=5,
            help=(
                "Number of measured requests "
                "per page."
            ),
        )

    def handle(
        self,
        *args,
        **options,
    ):

        username = options[
            "username"
        ]

        runs = options[
            "runs"
        ]

        if runs < 1:

            raise CommandError(
                "Runs must be at least 1."
            )

        password = getpass(
            "Password: "
        )

        client = Client()

        logged_in = client.login(
            username=username,
            password=password,
        )

        if not logged_in:

            raise CommandError(
                "Login failed."
            )

        endpoints = [
            (
                "Dashboard",
                reverse(
                    "dashboard"
                ),
            ),
            (
                "Application List",
                reverse(
                    "application_list"
                ),
            ),
            (
                "Incident List",
                reverse(
                    "incident_list"
                ),
            ),
        ]

        application = (
            Application.objects
            .order_by("pk")
            .first()
        )

        if application:

            endpoints.append(
                (
                    "Application Detail",
                    reverse(
                        "application_detail",
                        args=[
                            application.pk
                        ],
                    ),
                )
            )

        incident = (
            Incident.objects
            .order_by("pk")
            .first()
        )

        if incident:

            endpoints.append(
                (
                    "Incident Detail",
                    reverse(
                        "incident_detail",
                        args=[
                            incident.pk
                        ],
                    ),
                )
            )

        self.stdout.write(
            ""
        )

        self.stdout.write(
            "Performance Test"
        )

        self.stdout.write(
            f"Measured runs per page: {runs}"
        )

        self.stdout.write(
            "Target: < 2000 ms"
        )

        self.stdout.write(
            ""
        )

        for name, url in endpoints:

            # Warm-up request.
            warmup = client.get(
                url,
                HTTP_HOST="localhost",
            )

            if (
                warmup.status_code
                != 200
            ):

                self.stdout.write(
                    self.style.ERROR(
                        (
                            f"{name}: "
                            f"warm-up returned "
                            f"HTTP "
                            f"{warmup.status_code}"
                        )
                    )
                )

                continue

            timings = []

            for _ in range(
                runs
            ):

                start = (
                    time.perf_counter()
                )

                response = client.get(
                    url,
                    HTTP_HOST="localhost",
                )

                end = (
                    time.perf_counter()
                )

                if (
                    response.status_code
                    != 200
                ):

                    raise CommandError(
                        (
                            f"{name} returned "
                            f"HTTP "
                            f"{response.status_code}"
                        )
                    )

                elapsed_ms = (
                    (end - start)
                    * 1000
                )

                timings.append(
                    elapsed_ms
                )

            average = (
                statistics.mean(
                    timings
                )
            )

            median = (
                statistics.median(
                    timings
                )
            )

            minimum = min(
                timings
            )

            maximum = max(
                timings
            )

            result = (
                "PASS"
                if maximum < 2000
                else "REVIEW"
            )

            formatted_runs = (
                ", ".join(
                    f"{value:.2f}"
                    for value
                    in timings
                )
            )

            self.stdout.write(
                ""
            )

            self.stdout.write(
                name
            )

            self.stdout.write(
                (
                    "Runs (ms): "
                    f"{formatted_runs}"
                )
            )

            self.stdout.write(
                (
                    "Average: "
                    f"{average:.2f} ms"
                )
            )

            self.stdout.write(
                (
                    "Median: "
                    f"{median:.2f} ms"
                )
            )

            self.stdout.write(
                (
                    "Minimum: "
                    f"{minimum:.2f} ms"
                )
            )

            self.stdout.write(
                (
                    "Maximum: "
                    f"{maximum:.2f} ms"
                )
            )

            if result == "PASS":

                self.stdout.write(
                    self.style.SUCCESS(
                        "Result: PASS"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        "Result: REVIEW"
                    )
                )