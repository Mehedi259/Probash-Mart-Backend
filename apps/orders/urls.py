from django.urls import path
from . import views

urlpatterns = [
    # Customer
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('my-orders/', views.MyOrdersView.as_view(), name='my-orders'),
    path('my-orders/<uuid:pk>/', views.MyOrderDetailView.as_view(), name='my-order-detail'),
    path('track/<str:order_number>/', views.OrderTrackView.as_view(), name='order-track'),

    # Admin
    path('admin/list/', views.AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<uuid:pk>/', views.AdminOrderDetailView.as_view(), name='admin-order-detail'),
]
