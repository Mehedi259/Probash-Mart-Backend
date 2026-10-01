from django.urls import path
from . import views

urlpatterns = [
    path('', views.ActiveBannersView.as_view(), name='banner-active'),
    path('admin/list/', views.AdminBannerListView.as_view(), name='admin-banner-list'),
    path('admin/<uuid:pk>/', views.AdminBannerDetailView.as_view(), name='admin-banner-detail'),
]
