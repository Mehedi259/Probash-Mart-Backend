from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminOrReadOnly
from .models import Banner
from .serializers import BannerSerializer


@extend_schema(tags=['Banners'])
class ActiveBannersView(generics.ListAPIView):
    """List active banners for the website."""
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        position = self.request.query_params.get('position', None)
        qs = Banner.objects.filter(is_active=True)
        if position:
            qs = qs.filter(position=position)
        return qs


@extend_schema(tags=['Banners'])
class AdminBannerListView(generics.ListCreateAPIView):
    """Admin: List or create banners."""
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title']


@extend_schema(tags=['Banners'])
class AdminBannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Update or delete banner."""
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
