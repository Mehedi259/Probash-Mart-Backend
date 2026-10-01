from django.urls import path
from . import views

urlpatterns = [
    # Admin routes first (to avoid slug conflict)
    path('admin/list/', views.AdminBlogPostListView.as_view(), name='admin-blog-list'),
    path('admin/<uuid:pk>/', views.AdminBlogPostDetailView.as_view(), name='admin-blog-detail'),

    # Public
    path('', views.BlogPostListView.as_view(), name='blog-list'),
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
]
