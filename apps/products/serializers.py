"""
Serializers for Product and Category.
"""

from django.db.models import Avg
from rest_framework import serializers
from .models import Product, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'image', 'description',
                  'is_active', 'sort_order', 'product_count']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'sort_order']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    in_stock = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'compare_price', 'image',
                  'weight', 'category', 'category_name', 'is_best_seller',
                  'is_featured', 'is_flash_deal', 'stock', 'stock_status',
                  'discount_percentage', 'in_stock', 'status', 'sold_count']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product detail view."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False)
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    in_stock = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(status='published')
        if reviews.exists():
            return round(reviews.aggregate(avg=Avg('rating'))['avg'], 1)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.filter(status='published').count()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin product creation/update."""

    class Meta:
        model = Product
        fields = ['name', 'description', 'short_description', 'price', 'compare_price',
                  'cost_price', 'category', 'image', 'stock', 'sku', 'weight', 'unit',
                  'is_best_seller', 'is_featured', 'is_flash_deal', 'flash_deal_end',
                  'status', 'meta_title', 'meta_description']
