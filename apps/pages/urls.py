from django.urls import path
from . import views

urlpatterns = [
    # Admin routes first (to avoid slug conflict)
    path('admin/list/', views.AdminPageListView.as_view(), name='admin-page-list'),
    path('admin/<uuid:pk>/', views.AdminPageDetailView.as_view(), name='admin-page-detail'),

    # Public
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page-detail'),
]
