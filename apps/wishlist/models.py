from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel


class WishlistItem(UUIDModel):
    """User's wishlist item."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='wishlist_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
