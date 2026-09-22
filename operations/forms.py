from django import forms

from .models import (
    Application,
    Incident,
)

from django.contrib.auth import (
    get_user_model,
)
from django.db.models import Q

from .services.permissions import (
    ADMINISTRATOR_GROUP,
    OPERATIONS_GROUP,
)

from .services.workflow import (
    get_allowed_transitions,
)

class ApplicationForm(forms.ModelForm):

    class Meta:

        model = Application

        fields = [
            "name",
            "description",
            "owner",
            "environment",
            "support_contact",
            "status",
            "availability_percentage",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "owner": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "environment": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "support_contact": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "availability_percentage":
                forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "min": "0",
                        "max": "100",
                        "step": "0.01",
                    }
                ),
        }


class IncidentCreateForm(forms.ModelForm):

    class Meta:

        model = Incident

        fields = [
            "application",
            "title",
            "description",
            "priority",
        ]

        widgets = {

            "application": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

class IncidentAssignmentForm(
    forms.ModelForm
):

    class Meta:

        model = Incident

        fields = [
            "assigned_user",
        ]

        widgets = {
            "assigned_user": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(
        self,
        *args,
        **kwargs,
    ):

        super().__init__(
            *args,
            **kwargs,
        )

        User = get_user_model()

        users = (
            User.objects
            .filter(
                is_active=True
            )
            .filter(
                Q(
                    is_superuser=True
                )
                |
                Q(
                    groups__name__in=[
                        ADMINISTRATOR_GROUP,
                        OPERATIONS_GROUP,
                    ]
                )
            )
            .distinct()
            .order_by(
                "username"
            )
        )

        self.fields[
            "assigned_user"
        ].queryset = users

        self.fields[
            "assigned_user"
        ].required = True


class IncidentTransitionForm(
    forms.Form
):

    new_status = forms.ChoiceField(
        label="New Status",
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    resolution_notes = forms.CharField(
        label="Resolution Notes",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
            }
        ),
    )

    def __init__(
        self,
        *args,
        incident,
        **kwargs,
    ):

        super().__init__(
            *args,
            **kwargs,
        )

        allowed = (
            get_allowed_transitions(
                incident
            )
        )

        labels = dict(
            Incident.Status.choices
        )

        self.fields[
            "new_status"
        ].choices = [
            (
                status,
                labels[status],
            )
            for status in allowed
        ]

        if (
            Incident.Status.RESOLVED
            not in allowed
        ):

            self.fields.pop(
                "resolution_notes"
            )

    def clean(self):

        cleaned_data = (
            super().clean()
        )

        new_status = (
            cleaned_data.get(
                "new_status"
            )
        )

        if (
            new_status
            == Incident.Status.RESOLVED
        ):

            notes = (
                cleaned_data.get(
                    "resolution_notes",
                    "",
                )
                .strip()
            )

            if not notes:

                self.add_error(
                    "resolution_notes",
                    (
                        "Resolution notes "
                        "are required."
                    ),
                )

        return cleaned_data