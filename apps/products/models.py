"""
Product and Category models for the Probash Mart catalog.
"""

from django.db import models
from django.utils.text import slugify
from apps.core.models import UUIDModel


class Category(UUIDModel):
    """Product category."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Lucide icon name')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        return self.products.count()


class Product(UUIDModel):
    """Product in the Probash Mart catalog."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        DRAFT = 'draft', 'Draft'

    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         help_text='Original price for discount display')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                  related_name='products')

    # Media
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Inventory
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, help_text='Display weight e.g. (500g)')
    unit = models.CharField(max_length=50, blank=True, default='piece')

    # Flags
    is_best_seller = models.BooleanField(default=False, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_flash_deal = models.BooleanField(default=False, db_index=True)
    flash_deal_end = models.DateTimeField(null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE,
                               db_index=True)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    # Stats
    views_count = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['category', 'status']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return round((1 - self.price / self.compare_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def stock_status(self):
        if self.stock == 0:
            return 'Out of Stock'
        elif self.stock <= 10:
            return 'Low Stock'
        return 'Active'


class ProductImage(UUIDModel):
    """Additional images for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.name} - Image {self.sort_order}"
