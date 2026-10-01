"""
Analytics views providing dashboard metrics for the admin panel.
Aggregates data from Orders, Products, Users, etc.
"""

from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Avg, F, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from drf_spectacular.utils import extend_schema

from apps.core.permissions import IsAdminUser
from apps.orders.models import Order
from apps.products.models import Product
from apps.accounts.models import User


@extend_schema(tags=['Analytics'])
class DashboardMetricsView(APIView):
    """Admin: Get key dashboard metrics (revenue, orders, customers, products)."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        sixty_days_ago = now - timedelta(days=60)

        # Current period metrics
        current_orders = Order.objects.filter(created_at__gte=thirty_days_ago)
        current_revenue = current_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        current_order_count = current_orders.count()

        # Previous period metrics (for trend)
        prev_orders = Order.objects.filter(
            created_at__gte=sixty_days_ago, created_at__lt=thirty_days_ago
        )
        prev_revenue = prev_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        prev_order_count = prev_orders.count()

        # Calculate trends
        def calc_trend(current, previous):
            if previous == 0:
                return 100.0 if current > 0 else 0.0
            return round(((current - previous) / previous) * 100, 1)

        total_customers = User.objects.filter(role='customer').count()
        total_products = Product.objects.filter(status='active').count()

        return Response({
            'total_revenue': float(current_revenue),
            'revenue_trend': calc_trend(float(current_revenue), float(prev_revenue)),
            'total_orders': current_order_count,
            'orders_trend': calc_trend(current_order_count, prev_order_count),
            'total_customers': total_customers,
            'total_products': total_products,
        })


@extend_schema(tags=['Analytics'])
class SalesOverviewView(APIView):
    """Admin: Daily sales data for charts."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        now = timezone.now()
        start_date = now - timedelta(days=days)

        orders = Order.objects.filter(
            created_at__gte=start_date
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            revenue=Sum('total_amount'),
            order_count=Count('id')
        ).order_by('date')

        return Response(list(orders))


@extend_schema(tags=['Analytics'])
class OrdersByStatusView(APIView):
    """Admin: Order count grouped by status."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        status_counts = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')

        total = sum(item['count'] for item in status_counts)
        result = []
        for item in status_counts:
            pct = round((item['count'] / total * 100), 1) if total > 0 else 0
            result.append({
                'status': item['status'],
                'count': item['count'],
                'percentage': pct,
            })

        return Response(result)


@extend_schema(tags=['Analytics'])
class TopProductsView(APIView):
    """Admin: Top selling products."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        products = Product.objects.filter(
            status='active'
        ).order_by('-sold_count')[:limit].values(
            'id', 'name', 'image', 'sold_count', 'price'
        )

        result = []
        for p in products:
            result.append({
                **p,
                'revenue': float(p['price']) * p['sold_count'],
            })

        return Response(result)


@extend_schema(tags=['Analytics'])
class AnalyticsOverviewView(APIView):
    """Admin: Analytics page metrics (conversion rate, AOV, etc.)."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()
        total_visitors = Product.objects.aggregate(total=Sum('views_count'))['total'] or 1
        conversion_rate = round((total_orders / total_visitors) * 100, 2) if total_visitors > 0 else 0

        avg_order_value = Order.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0

        return Response({
            'conversion_rate': conversion_rate,
            'average_order_value': float(avg_order_value),
            'total_visitors': total_visitors,
            'total_orders': total_orders,
        })
