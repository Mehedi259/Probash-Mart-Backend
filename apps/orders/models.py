"""
Order and OrderItem models for e-commerce order management.
"""

import uuid
from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel


class Order(UUIDModel):
    """Customer order."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'

    class PaymentMethod(models.TextChoices):
        COD = 'cod', 'Cash on Delivery'
        BKASH = 'bkash', 'bKash'
        NAGAD = 'nagad', 'Nagad'
        SSLCOMMERZ = 'sslcommerz', 'SSLCommerz'
        STRIPE = 'stripe', 'Stripe'
        IDEAL = 'ideal', 'iDEAL'
        CREDIT_CARD = 'credit_card', 'Credit/Debit Card'

    # Order identification
    order_number = models.CharField(max_length=20, unique=True, editable=False)

    # Customer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='orders')

    # Shipping info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Bangladesh')

    # Financials
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices,
                                       default=PaymentMethod.COD)
    payment_status = models.CharField(max_length=20, default='pending')

    # Coupon
    coupon_code = models.CharField(max_length=50, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING,
                               db_index=True)

    # Notes
    customer_note = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)

    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: PM-YYMMDD-XXXX
            import datetime
            today = datetime.date.today().strftime('%y%m%d')
            last_order = Order.objects.filter(
                order_number__startswith=f'PM-{today}'
            ).order_by('-order_number').first()
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.order_number = f'PM-{today}-{new_num:04d}'
        super().save(*args, **kwargs)

    @property
    def item_count(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0


class OrderItem(UUIDModel):
    """Individual item within an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=300)
    product_image = models.URLField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
