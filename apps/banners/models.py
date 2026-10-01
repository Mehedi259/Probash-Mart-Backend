from django.db import models
from apps.core.models import UUIDModel


class Banner(UUIDModel):
    """Promotional banner for the website."""

    class Position(models.TextChoices):
        HERO_SLIDER = 'hero_slider', 'Hero Slider'
        HEADER_TOP = 'header_top', 'Header Top'
        PROMO_SECTION = 'promo_section', 'Promo Section'
        SIDEBAR = 'sidebar', 'Sidebar'

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    position = models.CharField(max_length=20, choices=Position.choices, default=Position.HERO_SLIDER)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title
