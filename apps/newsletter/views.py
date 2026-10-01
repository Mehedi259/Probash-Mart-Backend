from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminUser
from .models import Subscriber
from .serializers import SubscriberSerializer


@extend_schema(tags=['Newsletter'])
class SubscribeView(generics.CreateAPIView):
    """Subscribe to newsletter (public)."""
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            return Response({'detail': 'Already subscribed!'}, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['Newsletter'])
class AdminSubscriberListView(generics.ListAPIView):
    """Admin: List all newsletter subscribers."""
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['email']
    filterset_fields = ['is_active']


@extend_schema(tags=['Newsletter'])
class UnsubscribeView(generics.DestroyAPIView):
    """Unsubscribe by email (sets inactive)."""
    permission_classes = [permissions.AllowAny]
    lookup_field = 'email'

    def get_queryset(self):
        return Subscriber.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
