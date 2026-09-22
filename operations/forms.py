from django import forms

from .models import Application


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