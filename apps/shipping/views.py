from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminOrReadOnly
from .models import ShippingZone
from .serializers import ShippingZoneSerializer


@extend_schema(tags=['Shipping'])
class ShippingZoneListView(generics.ListAPIView):
    """List active shipping zones (for checkout)."""
    serializer_class = ShippingZoneSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return ShippingZone.objects.filter(is_active=True)


@extend_schema(tags=['Shipping'])
class AdminShippingZoneListView(generics.ListCreateAPIView):
    """Admin: List or create shipping zones."""
    queryset = ShippingZone.objects.all()
    serializer_class = ShippingZoneSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=['Shipping'])
class AdminShippingZoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Update or delete shipping zone."""
    queryset = ShippingZone.objects.all()
    serializer_class = ShippingZoneSerializer
    permission_classes = [IsAdminOrReadOnly]
