from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminOrReadOnly
from .models import Page
from .serializers import PageSerializer


@extend_schema(tags=['Pages'])
class PageDetailView(generics.RetrieveAPIView):
    """Get a published page by slug (for website)."""
    serializer_class = PageSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Page.objects.filter(status='published')


@extend_schema(tags=['Pages'])
class AdminPageListView(generics.ListCreateAPIView):
    """Admin: List or create pages."""
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title']


@extend_schema(tags=['Pages'])
class AdminPageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Update or delete page."""
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsAdminOrReadOnly]
