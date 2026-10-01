from rest_framework import serializers
from .models import ShippingZone


class ShippingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingZone
        fields = ['id', 'name', 'estimated_time', 'fee', 'is_active']
