from django.db import models
from django.utils import timezone
from apps.core.models import UUIDModel


class Coupon(UUIDModel):
    """Discount coupon."""

    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        FIXED = 'fixed', 'Fixed Amount'

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(null=True, blank=True, help_text='Null = unlimited')
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.code

    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @property
    def is_valid(self):
        if not self.is_active:
            return False
        if self.is_expired:
            return False
        if self.max_uses and self.used_count >= self.max_uses:
            return False
        return True

    @property
    def status_display(self):
        if not self.is_active:
            return 'Inactive'
        if self.is_expired:
            return 'Expired'
        if self.max_uses and self.used_count >= self.max_uses:
            return 'Exhausted'
        return 'Active'

    @property
    def usage_display(self):
        max_str = str(self.max_uses) if self.max_uses else '∞'
        return f"{self.used_count} / {max_str}"
