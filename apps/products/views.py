"""
Views for Product and Category management.
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema

from apps.core.permissions import IsAdminOrReadOnly
from .models import Product, Category, ProductImage
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    CategorySerializer,
    ProductImageSerializer,
)


# ─── Product Views (Website) ───────────────────────────────────────────────

@extend_schema(tags=['Products'])
class ProductListView(generics.ListAPIView):
    """List products with filtering, searching, and ordering."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'category__slug': ['exact'],
        'category__name': ['exact', 'icontains'],
        'status': ['exact'],
        'is_best_seller': ['exact'],
        'is_featured': ['exact'],
        'is_flash_deal': ['exact'],
        'price': ['gte', 'lte'],
    }
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', 'sold_count', 'name']

    def get_queryset(self):
        return Product.objects.filter(status='active').select_related('category')


@extend_schema(tags=['Products'])
class ProductDetailView(generics.RetrieveAPIView):
    """Get product detail by slug or ID."""
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Product.objects.select_related('category').prefetch_related('images', 'reviews')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        Product.objects.filter(pk=instance.pk).update(views_count=instance.views_count + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=['Products'])
class FeaturedProductsView(generics.ListAPIView):
    """List featured products for homepage."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(
            status='active', is_featured=True
        ).select_related('category')[:12]


@extend_schema(tags=['Products'])
class BestSellerProductsView(generics.ListAPIView):
    """List best seller products."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(
            status='active', is_best_seller=True
        ).select_related('category')[:12]


@extend_schema(tags=['Products'])
class FlashDealProductsView(generics.ListAPIView):
    """List flash deal products."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(
            status='active', is_flash_deal=True
        ).select_related('category')[:12]


@extend_schema(tags=['Products'])
class ProductsByCategoryView(generics.ListAPIView):
    """List products filtered by category slug."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.kwargs.get('category_slug')
        return Product.objects.filter(
            status='active', category__slug=slug
        ).select_related('category')


# ─── Admin Product Views ───────────────────────────────────────────────────

@extend_schema(tags=['Products'])
class AdminProductListView(generics.ListCreateAPIView):
    """Admin: List all products or create new."""
    queryset = Product.objects.all().select_related('category')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category', 'is_best_seller', 'is_featured']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['price', 'stock', 'sold_count', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer


@extend_schema(tags=['Products'])
class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Get, update, or delete a product."""
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer


@extend_schema(tags=['Products'])
class ProductImageUploadView(generics.CreateAPIView):
    """Admin: Upload additional images for a product."""
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = Product.objects.get(pk=product_id)
        serializer.save(product=product)


# ─── Category Views ────────────────────────────────────────────────────────

@extend_schema(tags=['Categories'])
class CategoryListView(generics.ListAPIView):
    """List all active categories (for website)."""
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


@extend_schema(tags=['Categories'])
class AdminCategoryListView(generics.ListCreateAPIView):
    """Admin: List or create categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']


@extend_schema(tags=['Categories'])
class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Get, update, or delete a category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
