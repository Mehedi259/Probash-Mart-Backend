from django.urls import path
from . import views

urlpatterns = [
    path('product/<uuid:product_pk>/', views.ProductReviewsView.as_view(), name='product-reviews'),
    path('admin/list/', views.AdminReviewListView.as_view(), name='admin-review-list'),
    path('admin/<uuid:pk>/moderate/', views.AdminReviewModerateView.as_view(), name='admin-review-moderate'),
    path('admin/<uuid:pk>/delete/', views.AdminReviewDeleteView.as_view(), name='admin-review-delete'),
]
