from django.contrib import admin
from .models import ShippingZone

@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'estimated_time', 'fee', 'is_active']
    list_filter = ['is_active']
