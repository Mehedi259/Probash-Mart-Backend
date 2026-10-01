from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel


class CartItem(UUIDModel):
    """Server-side cart item for authenticated users."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='cart_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
