from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminUser, IsAdminOrReadOnly
from .models import Transaction, PaymentMethod
from .serializers import TransactionSerializer, PaymentMethodSerializer


@extend_schema(tags=['Payments'])
class TransactionListView(generics.ListAPIView):
    """Admin: List all transactions."""
    queryset = Transaction.objects.all().select_related('order')
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['status', 'method']
    search_fields = ['transaction_id', 'order__order_number']


@extend_schema(tags=['Payments'])
class TransactionDetailView(generics.RetrieveAPIView):
    """Admin: Get transaction detail."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['Payments'])
class PaymentMethodListView(generics.ListCreateAPIView):
    """List or create payment methods."""
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=['Payments'])
class PaymentMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Update or delete payment method."""
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAdminOrReadOnly]
