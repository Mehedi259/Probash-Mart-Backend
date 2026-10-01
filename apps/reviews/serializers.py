from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'product_name', 'user', 'user_name',
                  'rating', 'comment', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status']


class ReviewModerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['status']
