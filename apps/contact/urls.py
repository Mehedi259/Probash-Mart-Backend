from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.ContactSubmitView.as_view(), name='contact-submit'),
    path('admin/list/', views.AdminContactListView.as_view(), name='admin-contact-list'),
    path('admin/<uuid:pk>/', views.AdminContactDetailView.as_view(), name='admin-contact-detail'),
]
