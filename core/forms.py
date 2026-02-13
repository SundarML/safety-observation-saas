from django import forms
from .models import DemoRequest
from django.contrib.auth import get_user_model 
from core.models import Organization

User = get_user_model()

class OrganizationSignupForm(forms.Form):
    organization_name = forms.CharField(max_length=255)
    domain = forms.CharField(max_length=255)
    # username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_domain(self):
        domain = self.cleaned_data["domain"].lower().strip()

        if Organization.objects.filter(domain=domain).exists():
            raise forms.ValidationError(
                "An organization with this domain already exists. Please log in or contact support."
            )

        return domain

    def clean(self):
        cleaned = super().clean()
        if cleaned['password1'] != cleaned['password2']:
            raise forms.ValidationError("Passwords do not match")
        return cleaned

class DemoRequestForm(forms.ModelForm):
    class Meta:
        model = DemoRequest
        fields = [
            "full_name",
            "email",
            "whatsapp_number",
            "company",
            "job_title",
            "message",
        ]

        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Tell us about your safety challenges (optional)"
            }),
        }

from .models import UserInvite

class InviteUserForm(forms.ModelForm):
    class Meta:
        model = UserInvite
        fields = ["email", "role"]


class AcceptInviteForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned["password1"] != cleaned["password2"]:
            raise forms.ValidationError("Passwords do not match")
        return cleaned