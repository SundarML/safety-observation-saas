from django.db import models
from django.utils import timezone
# Create your models here.

from django.db import models
import uuid


class UserInvite(models.Model):
    organization = models.ForeignKey(
        "core.Organization",
        on_delete=models.CASCADE
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=20,
        choices=[
            ("observer", "Observer"),
            ("action_owner", "Action Owner"),
            ("manager", "Manager"),
        ]
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        # return not self.is_used and self.expires_at > timezone.now()
        return not self.is_used and (self.expires_at is None or self.expires_at > timezone.now())
    def __str__(self):
        return f"{self.email} ({self.organization})"



class DemoRequest(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    whatsapp_number = models.CharField(max_length=20)
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.company})"

# core/models.py for saas application
class Organization(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# create a model for subscription plans
class Plan(models.Model):
    name = models.CharField(max_length=50)
    price_monthly = models.DecimalField(max_digits=8, decimal_places=2)
    max_users = models.IntegerField()
    max_observations = models.IntegerField()
    advanced_dashboard = models.BooleanField(default=False)
    exports_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# create a model for organization subscriptions
class Subscription(models.Model):
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE
    )

    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)

    active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    stripe_customer_id = models.CharField(max_length=120, blank=True)
    stripe_subscription_id = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.organization} — {self.plan}"

