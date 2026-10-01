from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import CartItem
from .serializers import CartItemSerializer, CartItemUpdateSerializer


@extend_schema(tags=['Cart'])
class CartListView(generics.ListCreateAPIView):
    """List cart items or add a product to cart."""
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cart_total = sum(item.total_price for item in queryset)
        cart_count = sum(item.quantity for item in queryset)
        return Response({
            'items': serializer.data,
            'cart_total': float(cart_total),
            'cart_count': cart_count,
        })


@extend_schema(tags=['Cart'])
class CartItemUpdateView(generics.UpdateAPIView):
    """Update cart item quantity."""
    serializer_class = CartItemUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


@extend_schema(tags=['Cart'])
class CartItemDeleteView(generics.DestroyAPIView):
    """Remove an item from cart."""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


@extend_schema(tags=['Cart'])
class CartClearView(APIView):
    """Clear all items from cart."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({'detail': 'Cart cleared.'}, status=status.HTTP_204_NO_CONTENT)
