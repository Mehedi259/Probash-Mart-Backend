from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminUser, IsAdminOrReadOnly
from .models import Coupon
from .serializers import CouponSerializer, CouponValidateSerializer


@extend_schema(tags=['Coupons'])
class CouponValidateView(APIView):
    """Validate a coupon code for checkout."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        order_total = serializer.validated_data['order_total']

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return Response({'detail': 'Invalid coupon code.'}, status=status.HTTP_404_NOT_FOUND)

        if not coupon.is_valid:
            return Response({'detail': f'Coupon is {coupon.status_display}.'}, status=status.HTTP_400_BAD_REQUEST)

        if order_total < coupon.min_order_amount:
            return Response({'detail': f'Minimum order amount is ৳{coupon.min_order_amount}.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if coupon.discount_type == 'percentage':
            discount = order_total * coupon.discount_value / 100
        else:
            discount = coupon.discount_value

        return Response({
            'valid': True,
            'code': coupon.code,
            'discount_type': coupon.discount_type,
            'discount_value': float(coupon.discount_value),
            'discount_amount': float(discount),
            'new_total': float(order_total - discount),
        })


@extend_schema(tags=['Coupons'])
class AdminCouponListView(generics.ListCreateAPIView):
    """Admin: List or create coupons."""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['code']
    filterset_fields = ['is_active', 'discount_type']


@extend_schema(tags=['Coupons'])
class AdminCouponDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Update or delete coupon."""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]
