from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('admin/list/', views.AdminCategoryListView.as_view(), name='admin-category-list'),
    path('admin/<uuid:pk>/', views.AdminCategoryDetailView.as_view(), name='admin-category-detail'),
]
