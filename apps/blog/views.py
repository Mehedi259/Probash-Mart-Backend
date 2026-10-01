from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminOrReadOnly
from .models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer


@extend_schema(tags=['Blog'])
class BlogPostListView(generics.ListAPIView):
    """List published blog posts."""
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return BlogPost.objects.filter(status='published')


@extend_schema(tags=['Blog'])
class BlogPostDetailView(generics.RetrieveAPIView):
    """Get blog post detail by slug."""
    serializer_class = BlogPostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(status='published')


@extend_schema(tags=['Blog'])
class AdminBlogPostListView(generics.ListCreateAPIView):
    """Admin: List or create blog posts."""
    queryset = BlogPost.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'content']
    filterset_fields = ['status', 'category']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=['Blog'])
class AdminBlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Update or delete blog post."""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
