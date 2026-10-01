from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    status_display = serializers.ReadOnlyField()
    usage_display = serializers.ReadOnlyField()
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'min_order_amount',
                  'max_uses', 'used_count', 'is_active', 'expires_at',
                  'status_display', 'usage_display', 'is_valid', 'created_at']


class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField()
    order_total = serializers.DecimalField(max_digits=10, decimal_places=2)
