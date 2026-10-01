"""
Views for Order management.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.core.permissions import IsAdminUser, IsOwnerOrAdmin
from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    OrderStatusUpdateSerializer,
)


@extend_schema(tags=['Orders'])
class OrderCreateView(generics.CreateAPIView):
    """Create a new order (checkout)."""
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=['Orders'])
class MyOrdersView(generics.ListAPIView):
    """List orders for the authenticated user."""
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@extend_schema(tags=['Orders'])
class MyOrderDetailView(generics.RetrieveAPIView):
    """Get order detail for the authenticated user."""
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@extend_schema(tags=['Orders'])
class OrderTrackView(generics.RetrieveAPIView):
    """Track an order by order number (public)."""
    serializer_class = OrderListSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'order_number'

    def get_queryset(self):
        return Order.objects.all()


# ─── Admin Views ────────────────────────────────────────────────────────────

@extend_schema(tags=['Orders'])
class AdminOrderListView(generics.ListAPIView):
    """Admin: List all orders."""
    queryset = Order.objects.all().select_related('user')
    serializer_class = OrderListSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['status', 'payment_method', 'payment_status']
    search_fields = ['order_number', 'first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'total_amount']


@extend_schema(tags=['Orders'])
class AdminOrderDetailView(generics.RetrieveUpdateAPIView):
    """Admin: Get or update an order."""
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderStatusUpdateSerializer
        return OrderDetailSerializer
