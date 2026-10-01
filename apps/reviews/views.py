from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminUser
from .models import Review
from .serializers import ReviewSerializer, ReviewModerateSerializer


@extend_schema(tags=['Reviews'])
class ProductReviewsView(generics.ListCreateAPIView):
    """List published reviews or submit a review for a product."""
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return Review.objects.filter(product_id=product_id, status='published')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Reviews'])
class AdminReviewListView(generics.ListAPIView):
    """Admin: List all reviews with moderation."""
    queryset = Review.objects.all().select_related('product', 'user')
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['status', 'rating']
    search_fields = ['comment', 'product__name', 'user__email']


@extend_schema(tags=['Reviews'])
class AdminReviewModerateView(generics.UpdateAPIView):
    """Admin: Approve or reject a review."""
    queryset = Review.objects.all()
    serializer_class = ReviewModerateSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['Reviews'])
class AdminReviewDeleteView(generics.DestroyAPIView):
    """Admin: Delete a review."""
    queryset = Review.objects.all()
    permission_classes = [IsAdminUser]
