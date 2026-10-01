from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardMetricsView.as_view(), name='analytics-dashboard'),
    path('sales/', views.SalesOverviewView.as_view(), name='analytics-sales'),
    path('orders-by-status/', views.OrdersByStatusView.as_view(), name='analytics-orders-status'),
    path('top-products/', views.TopProductsView.as_view(), name='analytics-top-products'),
    path('overview/', views.AnalyticsOverviewView.as_view(), name='analytics-overview'),
]
