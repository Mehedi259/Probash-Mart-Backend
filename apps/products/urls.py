from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.ProductListView.as_view(), name='product-list'),
    path('featured/', views.FeaturedProductsView.as_view(), name='product-featured'),
    path('best-sellers/', views.BestSellerProductsView.as_view(), name='product-best-sellers'),
    path('flash-deals/', views.FlashDealProductsView.as_view(), name='product-flash-deals'),
    path('category/<slug:category_slug>/', views.ProductsByCategoryView.as_view(), name='product-by-category'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Admin
    path('admin/list/', views.AdminProductListView.as_view(), name='admin-product-list'),
    path('admin/<uuid:pk>/', views.AdminProductDetailView.as_view(), name='admin-product-detail'),
    path('admin/<uuid:product_pk>/images/', views.ProductImageUploadView.as_view(), name='admin-product-image-upload'),
]
