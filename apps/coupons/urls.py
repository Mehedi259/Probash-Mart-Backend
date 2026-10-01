from django.urls import path
from . import views

urlpatterns = [
    path('validate/', views.CouponValidateView.as_view(), name='coupon-validate'),
    path('admin/list/', views.AdminCouponListView.as_view(), name='admin-coupon-list'),
    path('admin/<uuid:pk>/', views.AdminCouponDetailView.as_view(), name='admin-coupon-detail'),
]
