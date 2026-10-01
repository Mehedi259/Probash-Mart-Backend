from django.db import models
from apps.core.models import UUIDModel


class Transaction(UUIDModel):
    """Payment transaction record."""

    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        PENDING = 'pending', 'Pending'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    transaction_id = models.CharField(max_length=100, unique=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE,
                               related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    gateway_response = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"


class PaymentMethod(UUIDModel):
    """Admin-configurable payment methods."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.name
