from django.core.exceptions import PermissionDenied
from observations.models import Observation

class OrganizationQuerySetMixin:
    """
    Ensures all Observation queries are tenant-scoped
    """

    def get_queryset(self):
        if not self.request.organization:
            raise PermissionDenied("No organization assigned")

        return Observation.objects.filter(
            organization=self.request.organization
        )
