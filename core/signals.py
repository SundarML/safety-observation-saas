from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization, Subscription, Plan


@receiver(post_save, sender=Organization)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        free_plan, _ = Plan.objects.get_or_create(name="Free")

        Subscription.objects.create(
            organization=instance,
            defaults = {
                "plan": free_plan}
        )
