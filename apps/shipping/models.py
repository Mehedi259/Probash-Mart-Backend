from django.db import models
from apps.core.models import UUIDModel


class ShippingZone(UUIDModel):
    """Shipping zone with delivery fee and time."""
    name = models.CharField(max_length=200)
    estimated_time = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['fee']

    def __str__(self):
        return self.name
