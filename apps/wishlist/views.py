from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import WishlistItem
from .serializers import WishlistItemSerializer


@extend_schema(tags=['Wishlist'])
class WishlistListView(generics.ListCreateAPIView):
    """List or add to wishlist."""
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Wishlist'])
class WishlistDeleteView(generics.DestroyAPIView):
    """Remove from wishlist."""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)


@extend_schema(tags=['Wishlist'])
class WishlistToggleView(APIView):
    """Toggle a product in/out of wishlist."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product')
        if not product_id:
            return Response({'detail': 'Product ID required.'}, status=status.HTTP_400_BAD_REQUEST)

        item, created = WishlistItem.objects.get_or_create(
            user=request.user, product_id=product_id
        )
        if not created:
            item.delete()
            return Response({'detail': 'Removed from wishlist.', 'in_wishlist': False})
        return Response({'detail': 'Added to wishlist.', 'in_wishlist': True},
                        status=status.HTTP_201_CREATED)
