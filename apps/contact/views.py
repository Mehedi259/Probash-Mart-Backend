from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminUser
from .models import ContactMessage
from .serializers import ContactMessageSerializer, ContactMessageUpdateSerializer


@extend_schema(tags=['Contact'])
class ContactSubmitView(generics.CreateAPIView):
    """Submit a contact message (public)."""
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Contact'])
class AdminContactListView(generics.ListAPIView):
    """Admin: List all contact messages."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['is_read', 'is_resolved']


@extend_schema(tags=['Contact'])
class AdminContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: View, update status, or delete a contact message."""
    queryset = ContactMessage.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ContactMessageUpdateSerializer
        return ContactMessageSerializer
