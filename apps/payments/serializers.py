from rest_framework import serializers
from .models import Transaction, PaymentMethod


class TransactionSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_id', 'order', 'order_number', 'amount',
                  'method', 'status', 'created_at']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description', 'is_active', 'sort_order']
