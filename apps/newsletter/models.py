from django.db import models
from apps.core.models import UUIDModel


class Subscriber(UUIDModel):
    """Newsletter subscriber."""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
