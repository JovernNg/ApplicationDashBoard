from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from operations.services.permissions import (
    ADMINISTRATOR_GROUP,
    OPERATIONS_GROUP,
)


class Command(BaseCommand):

    help = "Create the system user roles."

    def handle(self, *args, **options):

        groups = [
            ADMINISTRATOR_GROUP,
            OPERATIONS_GROUP,
        ]

        for group_name in groups:

            group, created = Group.objects.get_or_create(
                name=group_name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created role: {group.name}"
                    )
                )
            else:
                self.stdout.write(
                    f"Role already exists: {group.name}"
                )