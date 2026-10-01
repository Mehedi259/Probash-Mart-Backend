from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShippingZoneListView.as_view(), name='shipping-list'),
    path('admin/list/', views.AdminShippingZoneListView.as_view(), name='admin-shipping-list'),
    path('admin/<uuid:pk>/', views.AdminShippingZoneDetailView.as_view(), name='admin-shipping-detail'),
]
