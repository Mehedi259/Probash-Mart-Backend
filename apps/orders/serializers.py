"""
Serializers for Order management.
"""

from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image',
                  'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'total_price']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new order from checkout."""
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address',
                  'city', 'postal_code', 'payment_method', 'coupon_code',
                  'customer_note', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        # Calculate totals
        subtotal = sum(item['unit_price'] * item['quantity'] for item in items_data)
        shipping_fee = 50  # Default shipping fee
        total = subtotal + shipping_fee

        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total_amount=total,
            **validated_data
        )

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight order listing."""
    item_count = serializers.ReadOnlyField()
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer_name', 'total_amount',
                  'payment_method', 'status', 'item_count', 'created_at']

    def get_customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class OrderDetailSerializer(serializers.ModelSerializer):
    """Full order detail."""
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Admin: Update order status."""

    class Meta:
        model = Order
        fields = ['status', 'tracking_number', 'admin_note', 'payment_status']
